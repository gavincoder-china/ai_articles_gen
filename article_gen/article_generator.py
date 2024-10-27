import pandas as pd
from openai import OpenAI
import os
from datetime import datetime
from config import PROMPT_URL

class ArticleGenerator:
    def __init__(self, excel_path, output_folder, api_key):
        self.excel_path = excel_path
        self.output_folder = output_folder
        self.api_key = api_key
        
        # 确保输出文件夹存在
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # 读取系统提示词
        self.system_prompt = self.load_system_prompt()
        print("成功加载系统提示词")
        print(self.system_prompt)

    def load_system_prompt(self):
        """从文件加载系统提示词"""
        with open(PROMPT_URL, 'r', encoding='utf-8') as file:
            return file.read().strip()

    def read_topics(self):
        """读取Excel文件中的主题"""
        df = pd.read_excel(self.excel_path)
        # 假设主题在第一列
        return df.iloc[:, 0].dropna().tolist()
    
    def generate_article(self, topic):
        """调用OpenAI API生成文章"""
        prompt = f"""
        单词：{topic}
        """
        
        client = OpenAI(api_key=self.api_key, base_url="https://mtu.mtuopenai.xyz/v1")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )
        
        return response.choices[0].message.content
    
    def save_article(self, topic, content):
        """保存文章为Markdown文件"""
        # 处理文件名，移除非法字符
        safe_filename = "".join([c for c in topic if c.isalnum() or c in (' ', '-', '_')]).strip()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_filename}_{timestamp}.md"
        file_path = os.path.join(self.output_folder, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# {topic}\n\n")
            f.write(content)
        
        return file_path
    
    def run(self):
        """运行文章生成程序"""
        topics = self.read_topics()
        for topic in topics:
            try:
                print(f"正在生成文章：{topic}")
                content = self.generate_article(topic)
                file_path = self.save_article(topic, content)
                print(f"文章已保存：{file_path}")
            except Exception as e:
                print(f"生成文章 '{topic}' 时发生错误：{str(e)}")
