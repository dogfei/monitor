from flask import Flask, request
from dateutil import parser
import json
import yaml
import datetime
import smtplib
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from gevent.pywsgi import WSGIServer


def time_zone_conversion(utctime):
    format_time = parser.parse(utctime).strftime('%Y-%m-%dT%H:%M:%SZ')
    time_format = datetime.datetime.strptime(format_time, "%Y-%m-%dT%H:%M:%SZ")
    return str(time_format + datetime.timedelta(hours=8))


def get_email_conf(file, email_name=None, action=0):
    """
    :param file: yaml格式的文件类型
    :param email_name: 发送的邮件列表名
    :param action: 操作类型，0: 查询收件人的邮件地址列表, 1: 查询收件人的列表名称, 2: 获取邮件账号信息
    :return: 根据action的值，返回不通的数据结构
    """
    try:
        with open(file, 'r', encoding='utf-8') as fr:
            read_conf = yaml.safe_load(fr)
            if action == 0:
                for email in read_conf['email']:
                    if email['name'] == email_name:
                        return email['receive_addr']
                    else:
                        print("%s does not match for %s" % (email_name, file))
                else:
                    print("No recipient address configured")
            elif action == 1:
                return [items['name'] for items in read_conf['email']]
            elif action == 2:
                return read_conf['send']
    except KeyError:
        print("%s not exist" % email_name)
        exit(-1)
    except FileNotFoundError:
        print("%s file not found" % file)
        exit(-2)
    except Exception as e:
        raise e


def sendEmail(title, content, receivers=None):
    if receivers is None:
        receivers = ['chenf-o@glodon.com']
    send_dict = get_email_conf('email.yaml', action=2)
    mail_host = send_dict['smtp_host']
    mail_user = send_dict['send_user']
    mail_pass = send_dict['send_pass']
    sender = send_dict['send_addr']
    msg = MIMEText(content, 'html', 'utf-8')
    msg['From'] = "{}".format(sender)
    msg['To'] = ",".join(receivers)
    msg['Subject'] = title
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, msg.as_string())
        print('mail send successful.')
    except smtplib.SMTPException as e:
        print(e)


class ParseingTemplate:
    def __init__(self, templatefile):
        self.templatefile = templatefile

    def template(self, **kwargs):
        try:
            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template(self.templatefile)
            template_content = template.render(kwargs)
            return template_content
        except Exception as error:
            raise error


app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        prometheus_data = json.loads(request.data)
        # 时间转换，转换成东八区时间
        for k, v in prometheus_data.items():
            if k == 'alerts':
                for items in v:
                    if items['status'] == 'firing':
                        items['startsAt'] = time_zone_conversion(items['startsAt'])
                    else:
                        items['startsAt'] = time_zone_conversion(items['startsAt'])
                        items['endsAt'] = time_zone_conversion(items['endsAt'])
        team_name = prometheus_data["commonLabels"]["team"]
        generate_html_template_subj = ParseingTemplate('email_template_firing.html')
        html_template_content = generate_html_template_subj.template(
            prometheus_monitor_info=prometheus_data
        )
        # 获取收件人邮件列表
        email_list = get_email_conf('/usr/app/conf/email.yaml', email_name=team_name, action=0)
        sendEmail(
            'Prometheus Monitor',
            html_template_content,
            receivers=email_list
        )
        return "prometheus monitor"
    except Exception as e:
        raise e


if __name__ == '__main__':
    WSGIServer(('0.0.0.0', 5000), app).serve_forever()
