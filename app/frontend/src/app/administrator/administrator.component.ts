import { Component, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';

import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-administrator',
  templateUrl: './administrator.component.html',
  styleUrls: ['./administrator.component.css']
})
export class AdministratorComponent implements OnInit {

  private static ENDPOINT = "/../";

  token: string;

  firstname: string = '';
  lastname: string = '';
  password: string = '';

  constructor(private cookieService: CookieService, private http: HttpClient) {
    this.token = this.cookieService.get("token");
  }

  ngOnInit() {
    if(this.token != null) {

    }
  }

  signIn() {
    let instance = this;

    instance.http.put(AdministratorComponent.ENDPOINT + 'administrator/', {
      "firstname": instance.firstname,
      "lastname": instance.lastname,
      "password": instance.password,
    }).subscribe(resp => {
      instance.token = resp["uuid"];
    });
  }

  getHeader() {
    return {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'Token': this.token,
      }),
    };
  }

  signInDisabled() {
    return this.firstname == '' || this.lastname == '' || this.password == '';
  }

}
