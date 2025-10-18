import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VDSite.settings')
django.setup()


def debug_comment_api():
    base_url = 'http://localhost:8000/api/'

    # 首先获取文章列表，找到有效的文章ID
    posts_response = requests.get(base_url + 'posts/')
    if posts_response.status_code == 200:
        posts = posts_response.json()
        print(f"找到 {len(posts)} 篇文章")

        if posts:
            # 获取第一篇文章的详情
            first_post_id = posts[0]['id']
            print(f"测试文章 ID: {first_post_id}")

            # 测试评论提交
            comment_data = {
                "author_name": "测试用户",
                "content": "这是一条测试评论"
            }

            print(f"提交评论数据: {comment_data}")

            comment_response = requests.post(
                f"{base_url}posts/{first_post_id}/add_comment/",
                json=comment_data
            )

            print(f"评论响应状态: {comment_response.status_code}")
            print(f"评论响应内容: {comment_response.text}")

            if comment_response.status_code == 201:
                print("✓ 评论提交成功")
            else:
                print("✗ 评论提交失败")
        else:
            print("没有找到文章，请先创建测试数据")
    else:
        print(f"获取文章列表失败: {posts_response.status_code}")


if __name__ == '__main__':
    debug_comment_api()