import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-view-meeting',
  templateUrl: './view-meeting.component.html',
  styleUrls: ['./view-meeting.component.css']
})
export class ViewMeetingComponent implements OnInit {
  @Input() meeting;

  constructor() {
  }

  ngOnInit() {
  }

}
