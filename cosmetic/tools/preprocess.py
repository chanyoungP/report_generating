import pandas as pd
import re


class DataManager:
    def __init__(self, data_path: str):
        self.data_path = data_path

    def load_data(self) -> pd.DataFrame:
        "dataset path를 읽어서 pandas dataframe으로 반환"
        return pd.read_excel(self.data_path)

    # 특수문자를 제거하는 함수
    @staticmethod
    def remove_special_characters(text: str) -> str:
        return re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9\s]', '', text)

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        '''
        Input : pandas DataFrame
        Output : preprocessed pandas DataFrame

        - "[]"으로 입력된 데이터 제거
        - "price", "review_count" 컬럼 값을 숫자로 변환
        - "description", "tag" 컬럼의 특수문자 제거
        '''
        condition1 = (data["ingredient"] != '[]')
        condition2 = (data["description"] != '[]')
        condition3 = (data["tag"] != '[]')

        df = data[condition1 & condition2 & condition3]

        # Price ml 없애고 가격으로만 설정하고 타입변경
        df = df[~df['price'].str.contains('가격미정', na=False)]
        price = df['price'].str.split('/').str[-1].str[:-1].str.strip()
        df["price"] = price.str.replace(',', '').astype(int)

        # 리뷰 카운트도 리뷰 글자 없애고 타입변경
        review_count = df['review_count'].str.split(' ').str[-1]
        df["review_count"] = review_count.str.replace(',', '').astype(int)

        # 'description' 컬럼에서 특수문자 제거
        df['description'] = df['description'].apply(self.remove_special_characters)

        # tag 특수문자 제거
        df['tag'] = df['tag'].apply(self.remove_special_characters)

        return df

    def select_category(self, data: pd.DataFrame, category: str) -> pd.DataFrame:
        '''카테고리 입력하면 카테고리에 해당하는 row만 반환'''
        if category == "전체":
            return data
        else:
            category_condition = (data["category"] == category)
            sub_data = data.loc[category_condition]
            return sub_data

    def prepare_data(self, category: str) -> pd.DataFrame:
        '''data 전처리 과정을 한 번에 하는 함수'''
        data = self.load_data()
        data = self.preprocess_data(data)
        data = self.select_category(data, category)

        return data
