import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http'

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

  private static ENDPOINT = "/../";

  constructor(private http: HttpClient, private route: ActivatedRoute) {
    let instance = this;

    this.route.params.subscribe(params => {
        instance.uuid = params['uuid'];
        instance.http.get(CustomerComponent.ENDPOINT + "customer/" + this.uuid).subscribe(resp => {
          if(resp != null) {
            instance.email = resp["email"];
            instance.firstname = resp["firstname"];
            instance.lastname = resp["lastname"];
            instance.place = resp["place"];
            instance.address = resp["address"];
            instance.http.post(CustomerComponent.ENDPOINT + "ticket/customer/" + instance.uuid, '').subscribe(resp => {
              if(resp != null) {
                instance.tickets = resp["tickets"];

                instance.tickets.forEach(ticket => {
                  ticket["meeting"] = "";
                  ticket["price"] = "";

                  instance.http.get(CustomerComponent.ENDPOINT + "meeting/" + ticket.meeting_id).subscribe(resp => {
                    ticket["meeting"] = resp;
                  });
                  instance.http.get(CustomerComponent.ENDPOINT + "price/" + ticket.price_id).subscribe(resp => {
                    ticket["price"] = resp;
                  });
                });
              }
            });
          }
        });
    });
  }

  ngOnInit() {
  }

  deleteTicket(uuid) {
    let instance = this;
    instance.http.delete(CustomerComponent.ENDPOINT + "ticket/" + uuid).subscribe(resp => {
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
