# setup
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tools'))
)
from tools.preprocess import DataManager
# 엑셀 파일 로드
DATA_PATH = './data/cosmetic_data.xlsx'

datamanager = DataManager(DATA_PATH)


# test data load
def test_load_data():
    cosmetic_data = datamanager.load_data()
    assert len(cosmetic_data) > 0, "데이터 로드에 실패했습니다."


# test data preprocessing
def testPreprocessing():
    '''input으로 원천 데이터를 받으면 전처리된 데이터를 출력한다.'''
    data = datamanager.load_data()
    data = datamanager.preprocess_data(data)
    assert all(isinstance(x, int) or x is None for x in data['price'])


category = "스킨/토너"


def test_select_category():
    data = datamanager.load_data()
    data = datamanager.preprocess_data(data)
    data = datamanager.select_category(data, category)
    # 모든 행의 'category' 값이 입력한 category와 같은지 확인
    assert all(data["category"] == category)

    # 선택된 데이터가 비어있지 않은지 확인
    assert not data.empty, f"No data found for the category: {category}"
