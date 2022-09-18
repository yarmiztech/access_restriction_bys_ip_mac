
from odoo.addons.web.controllers import main
from odoo.http import request
from odoo.exceptions import Warning
import odoo
import odoo.modules.registry
from odoo.tools.translate import _
from odoo import http
class Home(main.Home):

    @http.route('/web/login', type='http', auth="public")
    def web_login(self, redirect=None, **kw):
        main.ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None
        if request.httprequest.method == 'POST':
            old_uid = request.uid
            ip_address = request.httprequest.environ['REMOTE_ADDR']
            if request.params['login']:
                user_rec = request.env['res.users'].sudo().search(
                    [('login', '=', request.params['login'])])
                if user_rec.allowed_ips:
                    ip_list = []
                    for rec in user_rec.allowed_ips:
                        ip_list.append(rec.ip_address)
                    if ip_address in ip_list:
                        try:
                            uid = request.session.authenticate(
                                request.session.db,
                                request.params[
                                    'login'],
                                request.params[
                                    'password'])
                            request.params['login_success'] = True
                            return http.redirect_with_hash(
                                self._login_redirect(uid, redirect=redirect))
                        except odoo.exceptions.AccessDenied as e:
                            request.uid = old_uid
                            if e.args == odoo.exceptions.AccessDenied().args:
                                values['error'] = _("Wrong login/password")
                    else:
                        request.uid = old_uid
                        values['error'] = _("Not allowed to login from this IP")
                # else:
                #     try:
                #         uid = request.session.authenticate(request.session.db,
                #                                            request.params[
                #                                                'login'],
                #                                            request.params[
                #                                                'password'])
                #         request.params['login_success'] = True
                #         return http.redirect_with_hash(
                #             self._login_redirect(uid, redirect=redirect))
                #     except odoo.exceptions.AccessDenied as e:
                #         request.uid = old_uid
                #         if e.args == odoo.exceptions.AccessDenied().args:
                #             values['error'] = _("Wrong login/password")
                if user_rec.allowed_macs:
                    mac_list = []
                    import uuid
                    # now_mac = str(uuid.getnode())
                    # from getmac import get_mac_address as gma
                    from uuid import getnode as get_mac

                    # now_mac = str(gma())
                    mac = get_mac()
                    now_mac = ':'.join(("%012X" % mac)[i:i + 2] for i in range(0, 12, 2))
                    # print(now_mac)
                    # now_mac = '5645654654654'
                    # for rec in user_rec.allowed_macs.filtered(lambda a: a.macs_address == str(now_mac)):
                    for rec in user_rec.allowed_macs:
                        mac_list.append(rec.macs_address)
                    if now_mac in mac_list:
                        try:
                            uid = request.session.authenticate(
                                request.session.db,
                                request.params[
                                    'login'],
                                request.params[
                                    'password'])
                            request.params['login_success'] = True
                            return http.redirect_with_hash(
                                self._login_redirect(uid, redirect=redirect))
                        except odoo.exceptions.AccessDenied as e:
                            request.uid = old_uid
                            if e.args == odoo.exceptions.AccessDenied().args:
                                values['error'] = _("Wrong login/password")
                    else:
                        # request.uid = old_uid
                        values['error'] = _("Not allowed to login from this MAC")
                else:
                    try:
                        uid = request.session.authenticate(request.session.db,
                                                           request.params[
                                                               'login'],
                                                           request.params[
                                                               'password'])
                        request.params['login_success'] = True
                        return http.redirect_with_hash(
                            self._login_redirect(uid, redirect=redirect))
                    except odoo.exceptions.AccessDenied as e:
                        request.uid = old_uid
                        if e.args == odoo.exceptions.AccessDenied().args:
                            values['error'] = _("Wrong login/password")


        return request.render('web.login', values)
