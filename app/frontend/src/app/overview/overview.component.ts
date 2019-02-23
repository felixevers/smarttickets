import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';

import * as data from '../endpoint.json';

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.css']
})
export class OverviewComponent implements OnInit {

  private static ENDPOINT = "/../";

  customer = '';
  meetings = [];

  constructor(private http: HttpClient, private route: ActivatedRoute, private router: Router) {
    let instance = this;

    this.getSetting('title', function(value) {
      if(value == '') {
          router.navigate(['/setup']);
      } else {
        instance.route.params.subscribe(params => {
          instance.customer = params['uuid'];

          if(instance.customer == null) {
            instance.customer = '';
          }
        });
      }
    });
  }

  ngOnInit() {
    this.getMeetings();
  }

  private getMeetings() {
    let obj = this;
    this.http.get(data["endpoint"] + "meeting/").subscribe(
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
    return this.http.get(data["endpoint"] + "meeting/" + uuid);
  }

  openDashboard() {
    this.router.navigate(['/customer/' + this.customer]);
  }

  getSetting(key, callback) {
    this.http.get(data["endpoint"] + 'setting/' + key).subscribe(resp => {
      callback(resp["value"]);
    });
  }

}
