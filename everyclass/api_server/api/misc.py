from flask_restplus import Namespace, Resource

api = Namespace('other', description='其他')


@api.route('/_search')
class Search(Resource):
    def get(self, classroom_id, semester):
        """
        搜索学生、老师、教室或课程
        """
        return {'res': classroom_id,
                'sem': semester}