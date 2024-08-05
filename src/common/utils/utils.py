import os


def read_qss(qss_file_path):
    if os.path.exists(qss_file_path):
        with open(qss_file_path, 'r', encoding='utf8') as f:
            stylesheet = f.read()
        return stylesheet
    else:
        return ""
