'''분포(그래프 그림)와 분포에 해당하는 정보(matrix)까지 받아야함. '''
# setup
import sys
import os
# 현재 파일의 경로를 기준으로 상위 디렉토리와 tools 디렉토리를 경로에 추가하여 preprocess.py를 import할 수 있도록 설정
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tools'))
)
from tools.preprocess import DataManager
from tools.visualize import VisualizeManager

DATA_PATH = './data/cosmetic_data.xlsx'
datamanager = DataManager(DATA_PATH)
data = datamanager.prepare_data(category="전체")
_FigPath = "/Users/bagchan-yeong/Desktop/cosmetic/graph"


def test_visualize():
    vis_manager = VisualizeManager(data=data)
    vis_manager.make_all_plot(_FigPath, use_column="description", n=30)
    assert os.path.exists(os.path.join(_FigPath, "price_distribution.png"))
    assert os.path.exists(os.path.join(_FigPath, "brand_distribution.png"))
    assert os.path.exists(
        os.path.join(_FigPath, "ingredients_distribution.png")
        )
    assert os.path.exists(
        os.path.join(_FigPath, "wordcloud.png")
        )
    assert os.path.exists(
        os.path.join(_FigPath, "lda_topic.png")
        )
