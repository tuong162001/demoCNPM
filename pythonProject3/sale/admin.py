from sale import app, db
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView
from sale.models import Category, Product, UserRole,Regulations,Receipt
from flask_login import current_user, logout_user
from flask import redirect
import utils
from datetime import datetime
from flask import request


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class ProductView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    column_exclude_list = ['image', 'active', 'created_date']
    column_labels = {
        'name': 'Ten san pham',
        'description': 'Mo ta',
        'price': 'Gia',
        'image': 'Anh',
        'category': 'Danh muc'

    }
    column_sortable_list = ['id', 'name', 'price']

class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):

        return self.render('admin/index.html', stats=utils.category_stats())


class StatsView(BaseView):
    @expose('/')

    def index(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        year = request.args.get('year', datetime.now().year)
        return self.render('admin/stats.html', month_stats=utils.product_month_stats(year=year), stats=utils.product_stats(kw=kw,
                                                                         from_date=from_date, to_date=to_date))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

admin = Admin(app=app, name="E-commerce Administration", template_mode='bootstrap4', index_view=MyAdminIndex())
admin.add_view(AuthenticatedModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(ModelView(Receipt, db.session))
admin.add_view(ModelView(Regulations, db.session))
admin.add_view(StatsView(name='Stats'))
admin.add_view(LogoutView(name='Logout'))


