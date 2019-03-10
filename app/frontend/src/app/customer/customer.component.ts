import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http'

import * as data from '../endpoint.json';

@Component({
  selector: 'app-customer',
  templateUrl: './customer.component.html',
  styleUrls: ['./customer.component.css']
})
export class CustomerComponent implements OnInit {

  uuid: string;
  email: string;
  firstname: string;
  lastname: string;
  place: string;
  address: string;

  tickets = [];
  buy_limit = -1;

  constructor(private http: HttpClient, private route: ActivatedRoute) {
    let instance = this;

    this.route.params.subscribe(params => {
        instance.getSetting('buy_limit', function(value) {
          if(!isNaN(value) && value >= 0) {
            instance.buy_limit = value;
          }
        });

        instance.uuid = params['uuid'];
        instance.http.get(data["endpoint"] + "customer/" + this.uuid).subscribe(resp => {
          if(resp != null) {
            instance.email = resp["email"];
            instance.firstname = resp["firstname"];
            instance.lastname = resp["lastname"];
            instance.place = resp["place"];
            instance.address = resp["address"];
            instance.http.post(data["endpoint"] + "ticket/customer/" + instance.uuid, '').subscribe(resp => {
              if(resp != null) {
                instance.tickets = resp["tickets"];

                instance.tickets.forEach(ticket => {
                  ticket["meeting"] = "";
                  ticket["price"] = "";
                  ticket["seat"] = "";

                  instance.http.get(data["endpoint"] + "seat/" + ticket.seat_id).subscribe(resp => {
                    ticket["seat"] = resp;
                  });
                  instance.http.get(data["endpoint"] + "meeting/" + ticket.meeting_id).subscribe(resp => {
                    ticket["meeting"] = resp;
                  });
                  instance.http.get(data["endpoint"] + "price/" + ticket.price_id).subscribe(resp => {
                    ticket["price"] = resp;
                  });
                });
              }
            });
          }
        });
    });
  }

  buyDisabled() {
    return this.buy_limit >= 0 && this.tickets.length >= this.buy_limit;
  }

  getSetting(key, callback) {
    this.http.get(data["endpoint"] + 'setting/' + key).subscribe(resp => {
      callback(resp["value"]);
    });
  }

  timeConverter(b) {
    var a = new Date(b*1000);

    var year = a.getFullYear();
    var month = String("0" + (a.getMonth() + 1)).slice(-2);
    var date = String("0" + a.getDate()).slice(-2);
    var hour = String("0" + a.getHours()).slice(-2);
    var min = String("0" + a.getMinutes()).slice(-2);

    var time = date + '.' + month + '.' + year + ' um ' + hour + ':' + min + ' Uhr'

    return time;
  }

  goToLink(url: string){
    window.open(data['endpoint'] + url, "_blank");
  }

  ngOnInit() {
  }

  deleteTicket(uuid) {
    let instance = this;
    instance.http.delete(data["endpoint"] + "ticket/" + uuid).subscribe(resp => {
      if(resp != null) {
        instance.tickets.forEach(ticket => {
          if(ticket.uuid == uuid) {
            instance.tickets.splice(instance.tickets.indexOf(ticket), 1);
          }
        })
      }
    });
  }

}
