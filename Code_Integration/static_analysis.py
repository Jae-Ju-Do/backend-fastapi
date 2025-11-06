import os, sys, joblib
import numpy as np
import pandas as pd
from extract_feature.function.extract_feature import ExtractFeatureFile
from sklearn.preprocessing import StandardScaler, Normalizer
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

# hex 데이터 int로 변경
def hex_to_decimal(hex_value):
    if isinstance(hex_value, str):
        try:
            if hex_value.startswith("0x"):
                hex_value = hex_value[2:]
            if hex_value == '0.0' or hex_value == '0':
                return 0
            return int(hex_value, 16)
        except ValueError as e:
            print(f"변환 오류 : {e}")
            return hex_value 
    return hex_value

# string 데이터 int로 변경
def string_to_int(hex_string):
    try:
        hex_bytes = hex_string.split()
        byte_array = bytes(int(x, 16) for x in hex_bytes)
        return int.from_bytes(byte_array, byteorder='big')
    except Exception as e:
        print(f"변환 오류: {e} - 값: {hex_string}")
        return 0

# bool 데이터 int로 변경 
def bool_to_int(data):
    bool_columns = data.select_dtypes(include=['bool'])
    data[bool_columns.columns] = bool_columns.astype(int)
    return data

def preprocess_feature_data(feature_data):
    feature_data = feature_data.fillna(0)  # NaN을 0으로 대체

    if "DOS_HEADER/e_res" in feature_data.columns:
        feature_data['DOS_HEADER/e_res'] = feature_data['DOS_HEADER/e_res'].apply(string_to_int)
    if "DOS_HEADER/e_res2" in feature_data.columns:
        feature_data['DOS_HEADER/e_res2'] = feature_data['DOS_HEADER/e_res2'].apply(string_to_int)

    feature_data = feature_data.applymap(hex_to_decimal)

    return feature_data

def static_analysis(dir, file_name):
    feature_data = ExtractFeatureFile(dir, file_name)

    model_dir = r"./model"
    model_files = [f for f in os.listdir(model_dir) if f.endswith('.pkl')]

    models = []
    results = {}
    for file in model_files:
        model_name = os.path.splitext(file)[0]
        model = joblib.load(os.path.join(model_dir, file))
        models.append(model_name)
        try:
            if isinstance(model, XGBClassifier):
                feature_names = model.get_booster().feature_names
                data = feature_data[feature_names]
            elif isinstance(model, LGBMClassifier):
                feature_names = model.feature_name_
                data = feature_data[feature_names]
            elif isinstance(model, CatBoostClassifier):
                feature_names = model.feature_names_
                data = feature_data[feature_names]
            else:
                feature_names = pd.read_csv(r"./model/train_columns.csv").columns
                data = feature_data[feature_names]
            data = preprocess_feature_data(data)
            results[model_name] = model.predict(data)

        except Exception as e:
            print(f"[{model_name}] 예측 중 오류 발생: {e}")
            results[model_name] = None
            return 2
    
    for model_name in models:
        print(f"{model_name} : {results[model_name][0]}")

    for model_name in models:
        if results[model_name][0] == 1:
            return 1

    return 0

# dir = r"./exe파일 모음"
# file_name = "../Lotto.exe"
# result = static_analysis(dir, file_name)  # 분석 실행

# print(result)  # 예측 결과 출력 (1 : 악성, 0 : 정상)
