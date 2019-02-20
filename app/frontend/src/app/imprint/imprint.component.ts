import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-imprint',
  templateUrl: './imprint.component.html',
  styleUrls: ['./imprint.component.css']
})
export class ImprintComponent implements OnInit {

  private static ENDPOINT = "/../";

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
    this.http.get(ImprintComponent.ENDPOINT + 'setting/' + key).subscribe(resp => {
      callback(resp["value"]);
    });
  }

}
