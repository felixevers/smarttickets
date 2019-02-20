import { Component } from '@angular/core';
import { Injectable } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
@Injectable()
export class AppComponent {

  private static ENDPOINT = "http://192.168.178.22:5000/";

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
    this.http.get(AppComponent.ENDPOINT + 'setting/' + key).subscribe(resp => {
      callback(resp["value"]);
    });
  }

}
