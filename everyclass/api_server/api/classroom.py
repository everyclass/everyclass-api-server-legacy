from flask_restplus import Namespace, Resource, fields

api = Namespace('classroom', description='教室相关')

classroom_fields = api.model('Classroom', {
    'id'      : fields.String(description='教室 ID', example='============'),
    'name'    : fields.String(description='教室名称', example='世B402'),
    'building': fields.String(description='教学楼', example='世纪楼'),
    'campus'  : fields.String(description='校区', example='铁道')
})

classroom_activity_fields = api.model('Classroom Activity', {
})


@api.route('/<string:classroom_id>/<string:semester>')
@api.doc(params={'classroom_id': '教室 ID',
                 'semester'    : '学期，格式为 2018-2019-1'})
class ClassroomActivity(Resource):
    @api.marshal_with(classroom_activity_fields)
    def get(self, classroom_id, semester):
        """
        获取教室活动
        """
        return {'res': classroom_id,
                'sem': semester}


@api.route('/<string:classroom_id>')
@api.doc(params={'classroom_id': '教室 ID'})
class Classroom(Resource):
    @api.marshal_with(classroom_fields)
    def get(self, classroom_id):
        """
        获取教室基本信息
        """
        return {'res': classroom_id}
