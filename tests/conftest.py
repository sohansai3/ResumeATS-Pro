import os
import tempfile

os.environ["DATABASE_URL"] = "sqlite:///" + tempfile.NamedTemporaryFile(suffix=".db", delete=False).name
os.environ["REPORT_DIR"] = tempfile.mkdtemp(prefix="ats-reports-")
