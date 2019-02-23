import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import * as data from '../endpoint.json';

@Component({
  selector: 'app-imprint',
  templateUrl: './imprint.component.html',
  styleUrls: ['./imprint.component.css']
})
export class ImprintComponent implements OnInit {

  text: string = '';

  constructor(private http: HttpClient) {
    let instance = this;

    this.getSetting('imprint', function(value) {
      instance.text = value;
    })
  }

  ngOnInit() {
  }

  getSetting(key, callback) {
    this.http.get(data["endpoint"] + 'setting/' + key).subscribe(resp => {
      callback(resp["value"]);
    });
  }

}
