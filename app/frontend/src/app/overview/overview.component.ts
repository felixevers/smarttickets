import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.css']
})
export class OverviewComponent implements OnInit {

  meetings = [];

  constructor(private http: HttpClient) { }

  ngOnInit() {
    this.getMeetings();
  }

  private getMeetings() {
    let obj = this;
    this.http.get("http://localhost:5000/meeting/").subscribe(
      resp => {
        let list = resp["meetings"];

        if(list != null) {
          list.forEach(function(uuid) {
            obj.getMeeting(uuid).subscribe(
              resp => {
                if(resp != null) {
                  obj.meetings.push(resp);
                }
              }
            );;
          });
        }
      }
    );
  }

  private getMeeting(uuid) {
    return this.http.get("http://localhost:5000/meeting/" + uuid);
  }

}
