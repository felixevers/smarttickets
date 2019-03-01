from flask import Flask, render_template, make_response
import pdfkit
from config import config
from api import api, db
from models.ticket import TicketModel
from models.meeting import MeetingModel
from models.seat import SeatModel
from models.price import PriceModel

from datetime import datetime

def register_download(app: Flask):

    @app.route('/download/<uuid>')
    def render_download(uuid):
        ticket = TicketModel.query.filter_by(uuid=uuid).first()

        if ticket:
            if ticket.paid:
                meeting = MeetingModel.query.filter_by(uuid=ticket.meeting_id).first()
                seat = SeatModel.query.filter_by(uuid=ticket.seat_id).first()
                seats = SeatModel.query.filter_by(block=seat.block, row=seat.row, room_id=meeting.room).all()
                price = PriceModel.query.filter_by(uuid=ticket.price_id).first()

                date = datetime.fromtimestamp(meeting.date).strftime('%d.%m.%Y um %H:%M Uhr')

                print([x.type for x in seats])

                data = [
                    'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCI+PGRlZnM+PHBhdGggaWQ9ImEiIGQ9Ik0wIDBoMjR2MjRIMFYweiIvPjwvZGVmcz48Y2xpcFBhdGggaWQ9ImIiPjx1c2UgeGxpbms6aHJlZj0iI2EiIG92ZXJmbG93PSJ2aXNpYmxlIi8+PC9jbGlwUGF0aD48cGF0aCBkPSJNNCAxOHYzaDN2LTNoMTB2M2gzdi02SDR6bTE1LThoM3YzaC0zek0yIDEwaDN2M0gyem0xNSAzSDdWNWMwLTEuMS45LTIgMi0yaDZjMS4xIDAgMiAuOSAyIDJ2OHoiIGNsaXAtcGF0aD0idXJsKCNiKSIvPjwvc3ZnPg==',
                    '',
                    'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0Ij48cGF0aCBkPSJNMCAwaDI0djI0SDB6IiBmaWxsPSJub25lIi8+PHBhdGggZD0iTTE5LjUxIDMuMDhMMy4wOCAxOS41MWMuMDkuMzQuMjcuNjUuNTEuOS4yNS4yNC41Ni40Mi45LjUxTDIwLjkzIDQuNDljLS4xOS0uNjktLjczLTEuMjMtMS40Mi0xLjQxek0xMS44OCAzTDMgMTEuODh2Mi44M0wxNC43MSAzaC0yLjgzek01IDNjLTEuMSAwLTIgLjktMiAydjJsNC00SDV6bTE0IDE4Yy41NSAwIDEuMDUtLjIyIDEuNDEtLjU5LjM3LS4zNi41OS0uODYuNTktMS40MXYtMmwtNCA0aDJ6bS05LjcxIDBoMi44M0wyMSAxMi4xMlY5LjI5TDkuMjkgMjF6Ii8+PC9zdmc+',
                    'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0Ij48cGF0aCBkPSJNMCAwaDI0djI0SDB6IiBmaWxsPSJub25lIi8+PHBhdGggZD0iTTE5LjUxIDMuMDhMMy4wOCAxOS41MWMuMDkuMzQuMjcuNjUuNTEuOS4yNS4yNC41Ni40Mi45LjUxTDIwLjkzIDQuNDljLS4xOS0uNjktLjczLTEuMjMtMS40Mi0xLjQxek0xMS44OCAzTDMgMTEuODh2Mi44M0wxNC43MSAzaC0yLjgzek01IDNjLTEuMSAwLTIgLjktMiAydjJsNC00SDV6bTE0IDE4Yy41NSAwIDEuMDUtLjIyIDEuNDEtLjU5LjM3LS4zNi41OS0uODYuNTktMS40MXYtMmwtNCA0aDJ6bS05LjcxIDBoMi44M0wyMSAxMi4xMlY5LjI5TDkuMjkgMjF6Ii8+PC9zdmc+',
                    'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0Ij48cGF0aCBmaWxsPSJub25lIiBkPSJNMCAwaDI0djI0SDB6Ii8+PGNpcmNsZSBjeD0iMTIiIGN5PSI0IiByPSIyIi8+PHBhdGggZD0iTTE5IDEzdi0yYy0xLjU0LjAyLTMuMDktLjc1LTQuMDctMS44M2wtMS4yOS0xLjQzYy0uMTctLjE5LS4zOC0uMzQtLjYxLS40NS0uMDEgMC0uMDEtLjAxLS4wMi0uMDFIMTNjLS4zNS0uMi0uNzUtLjMtMS4xOS0uMjZDMTAuNzYgNy4xMSAxMCA4LjA0IDEwIDkuMDlWMTVjMCAxLjEuOSAyIDIgMmg1djVoMnYtNS41YzAtMS4xLS45LTItMi0yaC0zdi0zLjQ1YzEuMjkgMS4wNyAzLjI1IDEuOTQgNSAxLjk1em0tNi4xNyA1Yy0uNDEgMS4xNi0xLjUyIDItMi44MyAyLTEuNjYgMC0zLTEuMzQtMy0zIDAtMS4zMS44NC0yLjQxIDItMi44M1YxMi4xYy0yLjI4LjQ2LTQgMi40OC00IDQuOSAwIDIuNzYgMi4yNCA1IDUgNSAyLjQyIDAgNC40NC0xLjcyIDQuOS00aC0yLjA3eiIvPjwvc3ZnPg==',
                ]

                color = [
                    'green',
                    'white',
                    'red',
                    'black',
                    'green',
                ]

                html = render_template('ticket.html', uuid=uuid, date=date, seats=seats, seat=seat, price=price, data=data, color=color)

                pdf = pdfkit.from_string(html, False)

                response = make_response(pdf)

                response.headers['Content-Type'] = 'application/pdf'
                response.headers['Content-Disposition'] = 'attachment; filename=ticket_' + ticket.uuid  + ".pdf"

                return response

        return '', 404
