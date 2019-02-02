import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-meeting',
  templateUrl: './meeting.component.html',
  styleUrls: ['./meeting.component.css']
})
export class MeetingComponent implements OnInit {

  uuid: string;
  name: string = "";
  description: string = "";

  room = [
    [
      [
        // block1
        {
          "icon": "event_seat"
        },
        {
          "icon": "event_seat",
          "reserved": true,
        },
      ],
      [
        {
          "icon": "event_seat"
        },
        {
          "icon": "event_seat"
        },
      ],
      [
        {
          "icon": "accessible"
        },
      ]
    ],
    [
      // block2
    ],
    [
      // block3

    ],
  ];

  private sub: any;

  constructor(private http: HttpClient, private route: ActivatedRoute) { }

  ngOnInit() {
    this.sub = this.route.params.subscribe(params => {
        this.uuid = params['uuid'];
        this.http.get("http://localhost:5000/meeting/" + this.uuid).subscribe(resp => {
          if(resp != null) {
            this.name = resp["name"];
            this.description = resp["description"];
          }
        })
    });
  }

  calcBlocks() {
    return this.room.length;
  }

}
