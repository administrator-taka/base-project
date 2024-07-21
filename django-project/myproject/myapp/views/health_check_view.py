import json

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from myapp.applications.application.service.channel_service import ChannelService
from myapp.applications.application.service.learning_language_service import LearningLanguageService
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myapp.applications.util.file_handler import FileHandler


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    youtube_download_service = ChannelService()
    channel_id = ''
    youtube_download_service.delete_channel_data(channel_id)
    return JsonResponse(data={"msg": "pass"}, status=200)


def test():
    # LanguageServiceのインスタンスを作成
    language_service = LearningLanguageService()

    # ダミーデータの作成
    dummy_user_id = "test_onigiri"
    dummy_documents = "サンプルのドキュメント"
    dummy_is_published = False
    dummy_language_code = YouTubeLanguage.ENGLISH

    # 新しいベース言語を作成
    language_service.create_base_language(
        dummy_user_id,
        dummy_language_code,
        dummy_documents,
        dummy_is_published,
        learning_language_documents='学習言語のドキュメント',
        learning_language_explanation='学習言語の説明',
        learning_language_video_id='learning_video_id',
        learning_language_timestamp_ms=1500
    )
    print("ベース言語が作成されました")

    # ベース言語一覧を取得
    base_language_list = language_service.get_base_language_list(dummy_user_id)
    print(f"ベース言語一覧: {base_language_list}")

    # 登録されたベース言語のIDを取得
    if base_language_list:
        created_base_language_id = base_language_list[0]['base_language_id']
    else:
        created_base_language_id = None
        print("ベース言語が一覧に見つかりません")

    # ベース言語の詳細を取得
    if created_base_language_id:
        base_language_detail = language_service.get_base_language_detail(created_base_language_id)
        print(f"ベース言語の詳細: {base_language_detail}")
    else:
        base_language_detail = "ベース言語が見つかりません"
        print(base_language_detail)

    # ベース言語を更新
    if created_base_language_id:
        language_service.update_base_language(
            created_base_language_id,
            "更新されたドキュメント",
            True
        )

        # 更新後のベース言語の詳細を取得
        updated_base_language_detail = language_service.get_base_language_detail(created_base_language_id)
        print(f"更新後のベース言語の詳細: {updated_base_language_detail}")
    else:
        updated_base_language_detail = "更新用のベース言語が見つかりません"
        print(updated_base_language_detail)

    # 新しい学習言語を作成
    learning_language_list = []  # 初期化
    updated_learning_language_detail = None  # 初期化

    if created_base_language_id:
        language_service.create_learning_language(
            created_base_language_id,
            dummy_language_code,
            '学習言語のドキュメント',
            explanation='学習言語の説明',
            video_id='learning_video_id',
            timestamp_ms=1500
        )
        print("学習言語が作成されました")

        # get_base_language_detail メソッドを使用して base_language の詳細情報を取得
        base_language_detail = language_service.get_base_language_detail(created_base_language_id)

        # 学習言語データを取得
        learning_language_list = base_language_detail.get('learning_languages_data', [])
        print(f"学習言語一覧: {learning_language_list}")

        # 学習言語を更新
        if learning_language_list:
            learning_language_id = learning_language_list[0]['learning_language_id']
            language_service.update_learning_language(
                learning_language_id,
                "更新されたドキュメント",
                "更新された説明",
                "updated_video_id",
                2000
            )

            # 更新後の学習言語の詳細を取得
            updated_learning_language_detail = language_service.get_learning_language_detail(learning_language_id)
            print(f"更新後の学習言語の詳細: {updated_learning_language_detail}")

            # 学習言語を削除
            language_service.delete_learning_language(learning_language_id)
            print("学習言語が削除されました")

        else:
            print("更新用の学習言語が見つかりません")

    # ベース言語を削除
    if created_base_language_id:
        language_service.delete_base_language(created_base_language_id)
        print("ベース言語が削除されました")

    # 最終確認としてベース言語と学習言語の詳細を取得（削除後は取得できないはず）
    try:
        deleted_base_language_detail = language_service.get_base_language_detail(created_base_language_id)
    except Exception as e:
        deleted_base_language_detail = "ベース言語が削除されました"
        print(f"エラー: {e}")

    print(f"削除されたベース言語の詳細: {deleted_base_language_detail}")

    try:
        deleted_learning_language_detail = language_service.get_learning_language_detail(learning_language_id)
    except Exception as e:
        deleted_learning_language_detail = "学習言語が削除されました"
        print(f"エラー: {e}")

    print(f"削除された学習言語の詳細: {deleted_learning_language_detail}")

    # 結果を返す
    response = JsonResponse(data={
        "msg": "正常に処理されました",
        "base_language_list": base_language_list,
        "base_language_detail": base_language_detail,
        "updated_base_language_detail": updated_base_language_detail,
        "learning_language_list": learning_language_list,
        "updated_learning_language_detail": updated_learning_language_detail,
        "deleted_base_language_detail": deleted_base_language_detail,
        "deleted_learning_language_detail": deleted_learning_language_detail,
    }, status=200)

    FileHandler.format_json_print(json.loads(response.content))
    return response
