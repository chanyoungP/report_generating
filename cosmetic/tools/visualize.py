'''분포(그래프 그림)와 분포에 해당하는 정보(matrix)까지 받아야함. '''
# setup
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib.font_manager as fm
import ast
from PIL import Image
from konlpy.tag import Mecab
import pandas as pd
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# # 한글 폰트 설정
# font_path = "/Users/bagchan-yeong/Library/Fonts/NanumBarunGothic.ttf"
# fontprop = fm.FontProperties(fname=font_path, size=12)
# plt.rc('font', family=fontprop.get_name())


class VisualizeManager:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.stopwords = set([
            '은', '는', '이', '가', '있', '하', '것', '들', '그', '되', '수', '이', '보',
            '않', '없', '나', '사람', '주', '아니', '등', '같', '우리', '때', '년', '가',
            '한', '지', '대하', '오', '말', '일', '그렇', '위하', '및', '경우', '그녀',
            '더', '또', '다', '같이', '이렇', '점', '그리고', '중', '그것', '잘', '두', '이런',
            '저', '걸', '와', '관하', '만', '이외', '어디',
            '내', '어떻게', '무엇', '여러', '좀', '이제', '어떤', '다시', '지금', '이곳', '거기',
            '정말', '어느', '그동안', '그것', '이렇게', '저것', '알', '모든', '그것', '다른', '가장',
            '우리', '대한', '그러나', '이것', '이렇게', '저것', '중', '한번', '다른', '나중', '하지만',
            '항상', '할수록', '피부', '제품', '사용', '도움', '개선', '동시', '효과', '전달', '적임',
            '완료', '가지', '케어', '로션', '리뉴얼', '이드', '토너', '크림', '마무리', '앰플',
            '에멀전', '에멀젼', '해결', '가득'
        ])
        self.mask_path = '/Users/bagchan-yeong/Desktop/cosmetic/mask/mask_image.png'
        self.font_path = "/Users/bagchan-yeong/Library/Fonts/NanumBarunGothic.ttf"
        self.fontprop = fm.FontProperties(fname=self.font_path, size=12)
        plt.rc('font', family=self.fontprop.get_name())

    def _price_dist_plot(self, save_path: str):
        plt.figure(figsize=(12, 8))
        sns.set_theme(style="whitegrid")
        sns.histplot(
            self.data["price"],
            kde=True,
            color="skyblue",
            edgecolor="black",
            linewidth=1.5
        )
        plt.title('Price Distribution', fontsize=20, weight='bold')
        plt.xlabel('Price', fontsize=15)
        plt.ylabel('Frequency', fontsize=15)

        # x축 눈금 설정 및 시각화 범위 제한
        plt.xlim(10000, 100000)
        step = 10000
        plt.xticks(np.arange(10000, 100000 + step, step), rotation=45)

        # 눈금 스타일 설정
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

        # 그래프 스타일 개선
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)

        plt.tight_layout()
        plt.savefig(os.path.join(save_path, "price_distribution.png"), dpi=300)

    def _brand_dist_plot(self, save_path: str, top_n: int):
        # 브랜드별 제품 수 카운트
        brand_counts = self.data['brand'].value_counts()

        # 상위 n개의 브랜드 추출
        top_n_brands = brand_counts.head(top_n)

        # Seaborn 스타일 설정
        sns.set_theme(style="whitegrid")

        # 막대 그래프 생성
        plt.figure(figsize=(14, 10))
        sns.barplot(
            x=top_n_brands.index,
            y=top_n_brands.values,
            palette="viridis"
        )

        plt.title(
            f'Top {top_n} Brands by Number of Products',
            fontsize=20, weight='bold', fontproperties=self.fontprop
        )
        plt.xlabel('Brand', fontsize=15, fontproperties=self.fontprop)
        plt.ylabel(
            'Number of Products', fontsize=15, fontproperties=self.fontprop
        )

        # x축 레이블 회전 및 정렬
        plt.xticks(
            rotation=45, ha='right', fontsize=12, fontproperties=self.fontprop
        )
        plt.yticks(
            fontsize=12, fontproperties=self.fontprop
        )

        # y축 그리드 스타일 설정
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # 상단과 우측의 축을 숨기기
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)

        plt.tight_layout()    # 그래프 저장
        plt.savefig(os.path.join(save_path, "brand_distribution.png"), dpi=300)

    # ingredient distribution top n by category
    def _ingre_dist_plot(self, save_path: str, top_n: int):
        ingredients = self.data['ingredient'].apply(ast.literal_eval).explode()
        # 성분별 카운트
        ingredient_counts = ingredients.value_counts()

        # 상위 n개의 성분 추출
        top_n_ingredients = ingredient_counts.head(top_n)

        # Seaborn 스타일 설정
        sns.set_theme(style="whitegrid")

        # 막대 그래프 생성
        plt.figure(figsize=(14, 10))
        sns.barplot(
            x=top_n_ingredients.values,
            y=top_n_ingredients.index,
            palette="viridis"
        )
        plt.title(
            f'Top {top_n} Ingredients by Frequency',
            fontsize=20,
            weight='bold',
            fontproperties=self.fontprop
        )
        plt.xlabel('Frequency', fontsize=15, fontproperties=self.fontprop)
        plt.ylabel('Ingredient', fontsize=15, fontproperties=self.fontprop)

        # y축 레이블 회전 및 정렬
        plt.xticks(fontsize=12, fontproperties=self.fontprop)
        plt.yticks(fontsize=12, fontproperties=self.fontprop)

        # x축 그리드 스타일 설정
        plt.grid(axis='x', linestyle='--', alpha=0.7)

        # 상단과 우측의 축을 숨기기
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)

        plt.tight_layout()

        # 그래프 저장
        plt.savefig(
            os.path.join(save_path, "ingredients_distribution.png"),
            dpi=300
        )

    def _make_word_cloud(self, save_path: str, use_column: str):
        word_mask = np.array(Image.open(self.mask_path))

        if use_column == "description":
            mecab = Mecab()
            text = " ".join(self.data['description'].dropna().astype(str))
            nouns = mecab.nouns(text)
            _words = [w for w in nouns if w not in self.stopwords and len(w) > 1]
            word_freq = pd.Series(_words).value_counts()

        elif use_column == "tag":
            tags = self.data['tag'].apply(ast.literal_eval).explode()
            word_freq = tags.value_counts()

        elif use_column == "ingredient":
            ingredients = self.data['ingredient'].apply(ast.literal_eval).explode()
            word_freq = pd.Series(ingredients).value_counts()

        else:
            raise NotImplementedError

        # 워드클라우드 생성
        wordcloud = WordCloud(
            font_path=self.font_path,
            width=800,
            height=400,
            mask=word_mask,
            max_words=500,
            background_color='white'
        ).generate_from_frequencies(word_freq)

        # 워드클라우드 시각화
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Word Cloud of {use_column}')
        # 그래프 저장
        plt.savefig(
            os.path.join(save_path, "wordcloud.png"),
            dpi=300
        )

    def _lda_topic_plot(self, save_path: str, n: int):
        mecab = Mecab()
        text = " ".join(self.data['description'].dropna().astype(str))
        nouns = mecab.nouns(text)
        _words = [w for w in nouns if w not in self.stopwords and len(w) > 1]
        vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words=list(self.stopwords))
        X = vectorizer.fit_transform(_words)

        # LDA 모델 훈련
        lda = LatentDirichletAllocation(n_components=n, random_state=42)
        lda.fit(X)
        feature_names = vectorizer.get_feature_names_out()

        fig, axes = plt.subplots(1, 5, figsize=(15, 10), sharex=True)
        axes = axes.flatten()
        for topic_idx, topic in enumerate(lda.components_):
            top_features_ind = topic.argsort()[:-10 - 1:-1]
            top_features = [feature_names[i] for i in top_features_ind]
            weights = topic[top_features_ind]

            ax = axes[topic_idx]
            ax.barh(top_features, weights, color='blue')
            ax.set_title(f'Topic {topic_idx + 1}')
            ax.invert_yaxis()
            ax.tick_params(axis='both', which='major', labelsize=10)
            for i in 'top right left'.split():
                ax.spines[i].set_visible(False)
            # x축, y축의 라벨에 폰트 적용
            ax.set_xlabel('Weight', fontproperties=self.fontprop)
            ax.set_ylabel('Words', fontproperties=self.fontprop)
            ax.set_yticklabels(top_features, fontproperties=self.fontprop)

        plt.suptitle("LDA TOPIC MODELING RESULT", fontsize=20, fontproperties=self.fontprop)
        plt.subplots_adjust(top=0.90, hspace=0.3)
        plt.savefig(
            os.path.join(save_path, "lda_topic.png"),
            dpi=300
        )

    def make_all_plot(self, save_path: str, use_column: str, n: int):
        self._price_dist_plot(save_path=save_path)
        self._brand_dist_plot(save_path=save_path, top_n=n)
        self._ingre_dist_plot(save_path=save_path, top_n=n)
        self._make_word_cloud(save_path=save_path, use_column=use_column)
        self._lda_topic_plot(save_path=save_path, n=5)
