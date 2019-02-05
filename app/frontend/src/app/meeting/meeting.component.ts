import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

import {MatSnackBar} from '@angular/material';


@Component({
  selector: 'app-meeting',
  templateUrl: './meeting.component.html',
  styleUrls: ['./meeting.component.css']
})
export class MeetingComponent implements OnInit {

  uuid: string;
  name: string = "";
  description: string = "";

  selected = [];

  room = [];

  private sub: any;

  constructor(private http: HttpClient, private route: ActivatedRoute, private snackBar: MatSnackBar) { }

  ngOnInit() {
    for(var b = 0; b < 3; b++) {
      this.room[b] = [];
      for(var r = 0; r < 10; r++) {
        this.room[b][r] = [];
        for(var s = 0; s < 10; s++) {
          this.room[b][r].push({
            "icon": "event_seat",
            "reserved": false,
            "price": 10,
          });
        }
      }
    }

    this.sub = this.route.params.subscribe(params => {
        this.uuid = params['uuid'];
        this.http.get("http://192.168.178.22:5000/meeting/" + this.uuid).subscribe(resp => {
          if(resp != null) {
            this.name = resp["name"];
            this.description = resp["description"];
          }
        })
    });
  }

  calcBlocks() {
    return 100 / this.room.length;
  }

  select(seat) {
    if(!seat.reserved) {
      if(this.selectedSeat(seat)) {
        this.selected.splice(this.selected.indexOf(seat), 1);
      } else {
        this.selected.push(seat);
      }
    }
  }

  selectedSeat(seat) {
    return this.selected.indexOf(seat) > -1;
  }

  getAmount() {
    let amount = 0;

    this.selected.forEach(function(seat) {
      amount += seat.price;
    });

    return amount;
  }

}
