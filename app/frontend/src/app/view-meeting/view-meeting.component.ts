import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-view-meeting',
  templateUrl: './view-meeting.component.html',
  styleUrls: ['./view-meeting.component.css']
})
export class ViewMeetingComponent implements OnInit {
  @Input() meeting;
  @Input() customer;

  date: Date = null;
  dateStr: string = "";

  start: Date = null;
  startStr: string = "";

  stop: Date = null;
  stopStr: string = "";

  constructor() {
  }

  ngOnInit() {
    this.date = new Date(this.meeting.date * 1000);
    this.dateStr = this.timeConverter(this.date);

    this.start = new Date(this.meeting.start * 1000);
    this.startStr = this.timeConverter(this.start);

    this.stop = new Date(this.meeting.stop * 1000);
    this.stopStr = this.timeConverter(this.stop);
  }

  timeConverter(a) {
    var year = a.getFullYear();
    var month = String("0" + (a.getMonth() + 1)).slice(-2);
    var date = String("0" + a.getDate()).slice(-2);
    var hour = String("0" + a.getHours()).slice(-2);
    var min = String("0" + a.getMinutes()).slice(-2);

    var time = date + '.' + month + '.' + year + ' um ' + hour + ':' + min + ' Uhr'

    return time;
  }

}
