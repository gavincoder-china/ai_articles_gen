from article_generator import ArticleGenerator
from config import OPENAI_API_KEY, EXCEL_PATH, OUTPUT_FOLDER, PROMPT_URL
import os

def load_prompt():
    """
    加载提示文件的内容
    
    Returns:
        str: 提示文件的内容
    """
    try:
        with open(PROMPT_URL, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"找不到提示文件：{PROMPT_URL}")

def main():
    try:
        generator = ArticleGenerator(
            excel_path=EXCEL_PATH,
            output_folder=OUTPUT_FOLDER,
            api_key=OPENAI_API_KEY
        )
        generator.run()
        print("所有文章生成完成！")
        # 测试加载提示词
        prompt = load_prompt()
        print("成功加载提示词")
    except Exception as e:
        print(f"程序运行出错：{str(e)}")

if __name__ == "__main__":
    main()
