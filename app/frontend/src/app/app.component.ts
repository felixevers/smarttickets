import { Component } from '@angular/core';
import { Injectable } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

import * as data from './endpoint.json';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
@Injectable()
export class AppComponent {

  title = 'smarttickets';

  public constructor(private http: HttpClient, private titleService: Title) {
    let instance = this;

    this.getSetting('title', function(title) {
      if(title == '') {
        title = 'Setup';
      }

      instance.setTitle(title);
      instance.title = title;
    });
  }

  public setTitle(newTitle: string) {
    this.titleService.setTitle(newTitle);
  }

  getSetting(key, callback) {
    this.http.get(data["endpoint"] + 'setting/' + key).subscribe(resp => {
      callback(resp["value"]);
    });
  }

}
