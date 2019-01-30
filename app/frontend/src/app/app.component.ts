import { Component } from '@angular/core';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
@Injectable()
export class AppComponent {

  title = 'smarttickets';
  meetings = [];

  public constructor(private titleService: Title, private http: HttpClient) {
    this.setTitle(this.title);
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

  public setTitle(newTitle: string) {
    this.titleService.setTitle(newTitle);
  }

}
