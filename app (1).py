import streamlit as st
import os
import shutil
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import asyncio

# Import your logic modules
from converter import OpenAIHandler
from analyzer import (
    load_source_config, determine_complexity, estimate_migration_time,
    count_objects, additional_insights
)
from etl_analyzer import (
    analyze_etl_complexity, analyze_datastage_complexity, count_complexity_levels, process_etl_results, convert_etl_results_to_csv
)
from codebase import process_etl_migration_new
from function_utils import extract_zip, create_zip, create_zip_all
import logging

load_dotenv()

# Directories
UPLOAD_DIR = "inputs_sqls"
OUTPUT_DIR = "outputs"
OPTIMIZED_OUTPUT_DIR = "optimized_outputs"
XML_UPLOAD_DIR = "input_xml"
XML_OUTPUT_DIR = "etl_converted_outputs"

# Ensure directories exist
for directory in [UPLOAD_DIR, OUTPUT_DIR, OPTIMIZED_OUTPUT_DIR, XML_UPLOAD_DIR, XML_OUTPUT_DIR]:
    os.makedirs(directory, exist_ok=True)

# Streamlit UI Setup
st.set_page_config(page_title="SQL & ETL Migration Suite", layout="wide")

st.sidebar.title("Migration Suite")
st.sidebar.markdown("---")

model_selection = st.sidebar.selectbox(
    "Select AI Model",
    ["gpt-4o", "Claude-Sonnet"],
    key="ai_model"
)
st.sidebar.markdown("---")

selected_option = st.sidebar.selectbox(
    "📌 Select a Module",
    [
        "SQL Complexity Analyzer",
        "SQL Conversion",
        "SQL Optimizer",
        "ETL Complexity Analyzer",
        "ETL Migration"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Module Description")
if selected_option == "SQL Complexity Analyzer":
    st.sidebar.info("Analyze SQL complexity and estimate migration effort")
elif selected_option == "SQL Conversion":
    st.sidebar.info("Convert SQL code between different database dialects")
elif selected_option == "SQL Optimizer":
    st.sidebar.info("Optimize your SQL queries for better performance")
elif selected_option == "ETL Complexity Analyzer":
    st.sidebar.info("Analyze ETL job complexity and estimate migration effort")
elif selected_option == "ETL Migration":
    st.sidebar.info("Convert ETL jobs to modern frameworks like PySpark or DBT")
st.sidebar.markdown("---")

module = selected_option

### 1. SQL Complexity Analyzer
if module == "SQL Complexity Analyzer":
    st.header("📊 SQL Complexity Analyzer")
    source_db = st.selectbox("Select the database dialect", ["teradata", "oracle", "sqlserver", "saphana"])
    uploaded_file = st.file_uploader("Upload ZIP containing SQL files", type=["zip"])
    analyze_button = st.button("🔍 Analyze Complexity", type="primary")

    if analyze_button:
        if not uploaded_file:
            st.error("Please upload a ZIP file of SQL scripts.")
            st.stop()
        try:
            # Clear and prepare input
            if os.path.exists(UPLOAD_DIR):
                shutil.rmtree(UPLOAD_DIR)
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            zip_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(zip_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            extract_zip(zip_path, UPLOAD_DIR)
            # Load source config
            _, config = load_source_config(source_db)
            complexity_weightage = config["COMPLEXITY_WEIGHTAGE"]
            complexity_range = config["COMPLEXITY_RANGE"]
            migration_time_hrs = config["MIGRATION_TIME_HRS"]
            exception_list = config["EXCEPTION_LIST_PS_WITH"].split(",")
            objects_list = config["OBJECTS"]
            # Analyze
            results = []
            complexity_counts = {"SIMPLE": 0, "MEDIUM": 0, "COMPLEX": 0, "VERY COMPLEX": 0, "UNKNOWN": 0}
            sql_files = list(Path(UPLOAD_DIR).rglob("*.sql"))
            for sql_file in sql_files:
                with open(sql_file, "r", encoding="utf-8") as f:
                    sql_code = f.read()
                obj_type = "FUNCTION" if "CREATE FUNCTION" in sql_code.upper() else \
                           "PROCEDURE" if "CREATE PROCEDURE" in sql_code.upper() else \
                           "VIEW" if "CREATE VIEW" in sql_code.upper() else "TABLE"
                complexity = determine_complexity(sql_code, obj_type, complexity_weightage, complexity_range)
                complexity_counts[complexity] += 1
                migration_time = estimate_migration_time(obj_type, complexity, migration_time_hrs)
                results.append({
                    "filename": sql_file.name,
                    "object_type": obj_type,
                    "complexity": complexity,
                    "estimated_migration_time": round(float(migration_time), 2) if migration_time else None
                })
            st.subheader("Results")
            st.table(results)
            st.subheader("Object Type Counts")
            object_counts = count_objects(UPLOAD_DIR, objects_list)
            st.table(object_counts)
            st.subheader("Additional Insights")
            insights = additional_insights(UPLOAD_DIR, exception_list)
            st.table(insights)
            st.subheader("Complexity Level Counts")
            st.table(complexity_counts)
        except Exception as e:
            st.error(f"Failed to analyze complexity: {e}")

### 2. SQL Conversion
elif module == "SQL Conversion":
    st.header("🔄 SQL Code Conversion")
    source_db = st.selectbox("Source Database", ["teradata", "oracle", "sqlserver", "saphana"])
    target_db = st.selectbox("Target Cloud", ["databricks", "bigquery", "snowflake"])
    uploaded_file = st.file_uploader("Upload ZIP file containing SQL files", type=["zip"])
    convert_button = st.button("🔄 Convert SQL Code", type="primary")

    if convert_button:
        if not uploaded_file:
            st.error("Please upload a ZIP file.")
            st.stop()
        # Validate
        if not (os.getenv("AZURE_OPENAI_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT")):
            st.error("OpenAI API Key or Endpoint not set in environment.")
            st.stop()
        try:
            if os.path.exists(UPLOAD_DIR):
                shutil.rmtree(UPLOAD_DIR)
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            zip_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(zip_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            extract_zip(zip_path, UPLOAD_DIR)
            openai_obj = OpenAIHandler()
            sql_files = list(Path(UPLOAD_DIR).rglob("*.sql"))
            progress_bar = st.progress(0)
            results = []
            for idx, sql_file in enumerate(sql_files):
                with open(sql_file, "r", encoding="utf-8") as f:
                    sql_code = f.read()
                converted_sql = openai_obj.convert_sql(sql_code, source_db, target_db, sql_file.name, "mapping")
                output_path = os.path.join(OUTPUT_DIR, sql_file.name)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(converted_sql)
                results.append({"filename": sql_file.name, "converted_sql": converted_sql})
                progress_bar.progress((idx + 1) / len(sql_files))
            st.success("Conversion complete!")
            st.json(results)
            converted_zip = create_zip(OUTPUT_DIR, "converted_sqls.zip", "sql")
            st.sidebar.download_button("Download Converted SQL", open(converted_zip, "rb"), file_name="converted_sqls.zip")
        except Exception as e:
            st.error(f"Conversion failed: {e}")

### 3. SQL Optimizer
elif module == "SQL Optimizer":
    st.header("⚡ SQL Query Optimizer")
    target_db = st.selectbox("Target Cloud Platform", ["databricks", "bigquery", "snowflake"])
    uploaded_file = st.file_uploader("Upload ZIP containing SQL files", type=["zip"])
    optimize_button = st.button("⚡ Optimize SQL Queries", type="primary")
    if optimize_button:
        if not uploaded_file:
            st.error("Please upload a ZIP file.")
            st.stop()
        # Validate
        if not (os.getenv("AZURE_OPENAI_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT")):
            st.error("OpenAI API Key or Endpoint not set in environment.")
            st.stop()
        try:
            if os.path.exists(OUTPUT_DIR):
                shutil.rmtree(OUTPUT_DIR)
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            zip_path = os.path.join(OUTPUT_DIR, uploaded_file.name)
            with open(zip_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            extract_zip(zip_path, OUTPUT_DIR)
            openai_obj = OpenAIHandler()
            sql_files = list(Path(OUTPUT_DIR).rglob("*.sql"))
            progress_bar = st.progress(0)
            results = []
            for idx, sql_file in enumerate(sql_files):
                with open(sql_file, "r", encoding="utf-8") as f:
                    sql_code = f.read()
                optimized_sql = openai_obj.optimize_sql_query(sql_code, target_db)
                output_path = os.path.join(OPTIMIZED_OUTPUT_DIR, sql_file.name)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(optimized_sql)
                results.append({"filename": sql_file.name, "optimized_sql": optimized_sql})
                progress_bar.progress((idx + 1) / len(sql_files))
            st.success("Optimization complete!")
            st.json(results)
            optimized_zip = create_zip(OPTIMIZED_OUTPUT_DIR, "optimized_sqls.zip", "sql")
            st.sidebar.download_button("Download Optimized SQL", open(optimized_zip, "rb"), file_name="optimized_sqls.zip")
        except Exception as e:
            st.error(f"Optimization failed: {e}")

### 4. ETL Complexity Analyzer
elif module == "ETL Complexity Analyzer":
    st.header("📊 ETL Complexity Analyzer")
    source = st.selectbox("Source ETL Tool", ["Informatica", "Datastage"])
    uploaded_file = st.file_uploader("Upload ZIP containing XML files", type=["zip"])
    analyze_button = st.button("📊 Analyze ETL Complexity", type="primary")
    if analyze_button:
        if not uploaded_file:
            st.error("Please upload a ZIP file.")
            st.stop()
        try:
            if os.path.exists(XML_UPLOAD_DIR):
                shutil.rmtree(XML_UPLOAD_DIR)
            os.makedirs(XML_UPLOAD_DIR, exist_ok=True)
            zip_path = os.path.join(XML_UPLOAD_DIR, uploaded_file.name)
            with open(zip_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            extract_zip(zip_path, XML_UPLOAD_DIR)
            results = []
            if source == "Datastage":
                for dirpath, _, filenames in os.walk(XML_UPLOAD_DIR):
                    for filename in filenames:
                        if filename.lower().endswith(".xml"):
                            full_path = os.path.join(dirpath, filename)
                            results.append(analyze_datastage_complexity(full_path))
                data_df, csv_data = process_etl_results(results)
                st.table(data_df)
            elif source == "Informatica":
                results = analyze_etl_complexity(XML_UPLOAD_DIR)
                csv_data = convert_etl_results_to_csv(results)
                csv_df = pd.read_csv(pd.compat.StringIO(csv_data))
                st.table(csv_df)
            st.sidebar.download_button(
                label="⬇️ Download CSV Report",
                data=csv_data,
                file_name="etl_complexity_report.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"ETL analysis failed: {e}")

### 5. ETL Migration
elif module == "ETL Migration":
    st.header("🔄 ETL Migration Tool")
    col1, col2 = st.columns(2)
    with col1:
        source_system = st.selectbox("ETL Source System", ["informatica", "datastage", "snowflake sql"])
    with col2:
        target_db = st.selectbox("Target", ["Snowpark Pyspark", "Snowflake SQL", "Matillion", "DBT"])
    file_type = st.selectbox("Output File Type", ["txt", "sql", "py", "xml", "json"])
    uploaded_zip = st.file_uploader("Upload ZIP File with XMLs", type=["zip"])

    # Instruction prompt (editable)
    if "instruction_prompt" not in st.session_state:
        from function_utils import generate_instruction
        st.session_state.instruction_prompt = generate_instruction(source_system, target_db, file_type)
        st.session_state.instruction_edited = False
    st.subheader("📝 Instruction Prompt")
    edited_prompt = st.text_area("Edit Instruction Prompt", st.session_state.instruction_prompt, height=300)
    if st.button("Save Instruction Prompt"):
        st.session_state.instruction_prompt = edited_prompt
        st.session_state.instruction_edited = True
        st.success("Instruction prompt updated.")

    generate_button = st.button("🔄 Start ETL Migration", type="primary")
    if generate_button:
        if not uploaded_zip:
            st.error("Please upload a ZIP file.")
            st.stop()
        # Check API keys for selected model
        def is_migration_api_ready(model_selection):
            if model_selection == "gpt-4o":
                return os.getenv("AZURE_OPENAI_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT")
            elif model_selection == "Claude-Sonnet":
                return os.getenv("DATABRICKS_PAT_TOKEN") and os.getenv("DATABRICKS_ENDPOINT")
            return False
        if not is_migration_api_ready(model_selection):
            st.error("API credentials missing for selected model.")
            st.stop()
        try:
            # Prepare directories
            if os.path.exists(XML_UPLOAD_DIR):
                shutil.rmtree(XML_UPLOAD_DIR)
            os.makedirs(XML_UPLOAD_DIR, exist_ok=True)
            if os.path.exists(XML_OUTPUT_DIR):
                shutil.rmtree(XML_OUTPUT_DIR)
            os.makedirs(XML_OUTPUT_DIR, exist_ok=True)
            zip_path = os.path.join(XML_UPLOAD_DIR, uploaded_zip.name)
            with open(zip_path, "wb") as f:
                f.write(uploaded_zip.getbuffer())
            extract_zip(zip_path, XML_UPLOAD_DIR)
            st.success("ZIP extracted successfully.")
            csv_data = []
            xml_files = [p for p in Path(XML_UPLOAD_DIR).rglob("*") if str(p).lower().endswith((".xml", ".sql"))]
            progress_bar = st.progress(0)
            for idx, xml_file in enumerate(xml_files):
                generated_code = process_etl_migration_new(
                    st.session_state.instruction_prompt,
                    xml_file,
                    source_system,
                    target_db,
                    model_selection
                )
                # Write output
                if generated_code:
                    output_path = os.path.join(XML_OUTPUT_DIR, xml_file.stem + f"_output.{file_type}")
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(generated_code)
                    csv_data.append({"File Name": xml_file.stem, "Output Path": output_path})
                progress_bar.progress((idx + 1) / len(xml_files))
            st.success("ETL conversion complete!")
            generated_zip = create_zip_all(XML_OUTPUT_DIR, "etl_converted_outputs.zip")
            st.sidebar.download_button(
                "📥 Download Outputs",
                open(generated_zip, "rb"),
                file_name="etl_converted_outputs.zip"
            )
        except Exception as e:
            st.error(f"ETL Migration failed: {e}")