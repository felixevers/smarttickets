import { Component, Inject, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';

import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';

import {FormControl} from '@angular/forms';
import {DateAdapter, MAT_DATE_FORMATS, MAT_DATE_LOCALE} from '@angular/material/core';

import * as data from '../endpoint.json';

@Component({
  selector: 'app-administrator',
  templateUrl: './administrator.component.html',
  styleUrls: ['./administrator.component.css'],
})
export class AdministratorComponent implements OnInit {

  token: string;
  headers;

  meetings = [];
  prices = [];
  rooms = [];

  selectedMeeting;
  selectedPrice;
  selectedRoom;
  selectedSeat;

  selectedMeetingDate = new Date();
  selectedMeetingSaleStart = new Date();
  selectedMeetingSaleStop = new Date();

  firstname: string = '';
  lastname: string = '';
  password: string = '';

  meetingName: string = '';
  meetingDescription: string = '';
  meetingSaleStart = new Date();
  meetingSaleStop = new Date();
  meetingDate = new Date();
  meetingRoom;

  priceName: string = '';
  priceDescription: string = '';
  priceValue = 0;

  roomName: string = '';

  seatRow;
  seatBlock;
  seatAccessible;

  settingKey: string = '';
  settingValue: string = '';
  settingBeforeValue: string = '';

  constructor(private cookieService: CookieService, private http: HttpClient) {
    this.token = this.cookieService.get("token");

    let instance = this;
    if(this.token != null) {
      instance.http.get(data["endpoint"] + 'administrator/session/', instance.getHeader()).subscribe(resp => {
        instance.firstname = resp["firstname"];
        instance.lastname = resp["lastname"];
        instance.getMeetings();
        instance.getPrices();
        instance.getRooms();
      });
    }
  }

  ngOnInit() {
  }

  getHeader() {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Token': this.token,
      }),
    };

    return httpOptions;
  }

  signInError() {
    this.firstname = '';
    this.lastname = '';
    this.password = '';
  }

  signIn() {
    let instance = this;

    instance.http.put(data["endpoint"] + 'administrator/session/', {
      "firstname": instance.firstname,
      "lastname": instance.lastname,
      "password": instance.password,
    }).subscribe(resp => {
      if(!resp["result"]) {
        instance.signInError();
      } else {
        instance.token = resp["uuid"];
      }
    });
  }

  private createMeeting() {
    let instance = this;

    instance.http.put(data["endpoint"] + 'meeting/', {
      "name": instance.meetingName,
      "description": instance.meetingDescription,
      "room": instance.meetingRoom, // TODO EDIT!
      "date": (instance.meetingDate.getTime() / 1000),
      "start": (instance.meetingSaleStart.getTime() / 1000),
      "stop": (instance.meetingSaleStop.getTime() / 1000),
    }, instance.getHeader()).subscribe(resp => {
      instance.meetingName = '';
      instance.meetingDescription = '';
      instance.meetingRoom = null;
      instance.meetingDate = null;
      instance.meetingSaleStart = null;
      instance.meetingSaleStop = null;
      instance.getMeetings();
    });
  }

  private disableMeeting() {
    return this.meetingName == '' || this.meetingName == null || this.meetingDescription == '' || this.meetingDescription == null || this.meetingRoom == '' || this.meetingRoom == null;
  }

  private createPrice() {
    let instance = this;

    instance.http.put(data["endpoint"] + 'price/', {
      "name": instance.priceName,
      "description": instance.priceDescription,
      "value": instance.priceValue,
    }, instance.getHeader()).subscribe(resp => {
      instance.priceName = '';
      instance.priceDescription = '';
      instance.priceValue= 0;
      instance.getPrices();
    });
  }

  private disablePrice() {
    return this.priceName == '' || this.priceName == null || this.priceDescription == '' || this.priceDescription == null || this.priceValue == null;
  }

  private createRoom() {
    let instance = this;
    instance.http.put(data["endpoint"] + 'room/', {
      "name": instance.roomName,
    }, instance.getHeader()).subscribe(resp => {
      instance.roomName = '';
      instance.getRooms();
    });
  }

  private disableRoom() {
    return this.roomName == '' || this.roomName == null;
  }

  private createSeat() {
    let instance = this;

    instance.http.put(data["endpoint"] + 'seat/', {
      "room": instance.selectedRoom.uuid,
      "block": instance.seatBlock - 1,
      "row": instance.seatRow - 1,
      "accessible": instance.seatAccessible,
    }, instance.getHeader()).subscribe(resp => {
      console.log(resp);
    });
  }

  private disableSeat() {
    return this.seatBlock == null || this.seatRow == null || this.seatAccessible == null;
  }

  private getRooms() {
    let instance = this;

    instance.rooms = [];

    instance.http.get(data["endpoint"] + 'room/').subscribe(resp => {
      [].concat(resp).forEach(e => {
        instance.rooms.push(e);
      })
    });
  }

  private getPrices() {
    let instance = this;

    instance.prices = [];

    instance.http.get(data["endpoint"] + 'price/').subscribe(resp => {
      instance.prices = resp["prices"];
    });
  }

  private getMeetings() {
    let obj = this;

    this.meetings = [];

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

  signInDisabled() {
    return this.firstname == '' || this.lastname == '' || this.password == '';
  }

  private refreshSetting() {
    let instance = this;

    instance.http.get(data["endpoint"] + 'setting/' + instance.settingKey).subscribe(resp => {
      instance.settingBeforeValue = resp["value"];
      instance.settingValue = resp["value"];
    });
  }

  private updateSetting() {
    let instance = this;

    instance.http.post(data["endpoint"] + 'setting/', {
      "key": instance.settingKey,
      "value": instance.settingValue,
    }, instance.getHeader()).subscribe(resp => {
      if(resp["result"] != null && !resp["result"]) {
        instance.http.put(data["endpoint"] + 'setting/', {
          "key": instance.settingKey,
          "value": instance.settingValue,
        }, instance.getHeader()).subscribe(resp => {
          instance.settingBeforeValue = instance.settingValue;
        });
      } else {
        instance.settingBeforeValue = instance.settingValue;
      }
    });
  }

  private disableSetting() {
    return this.settingKey == '' || this.settingKey == null || this.settingValue == this.settingBeforeValue;
  }

  private update() {
    let instance = this;
    if(instance.selectedPrice != null) {
      instance.http.post(data["endpoint"] + 'price/' + instance.selectedPrice.uuid, {
        "name": instance.selectedPrice.name,
        "description": instance.selectedPrice.description,
        "value": instance.selectedPrice.value,
      }, instance.getHeader()).subscribe(resp => {
        instance.selectedPrice = null;
        instance.getPrices();
      });
    }
    if(instance.selectedMeeting != null) {
      instance.http.post(data["endpoint"] + 'meeting/' + instance.selectedMeeting.uuid, {
        "name": instance.selectedMeeting.name,
        "description": instance.selectedMeeting.description,
        "room": instance.selectedMeeting.room,
        "date": instance.selectedMeeting.date,
        "start": instance.selectedMeeting.start,
        "stop": instance.selectedMeeting.stop,
      }, instance.getHeader()).subscribe(resp => {
        instance.selectedMeeting = null;
        instance.selectedMeetingDate = new Date();
        instance.selectedMeetingSaleStart = new Date();
        instance.selectedMeetingSaleStop = new Date();

        instance.getMeetings();
      });
    }
  }

  private delete() {
    let instance = this;
    if(instance.selectedPrice != null) {
      instance.http.delete(data["endpoint"] + 'price/' + instance.selectedPrice.uuid, instance.getHeader()).subscribe(resp => {
        instance.selectedPrice = null;
        instance.getPrices();
      });
    }
    if(instance.selectedRoom != null) {
      instance.http.delete(data["endpoint"] + 'room/' + instance.selectedRoom.uuid, instance.getHeader()).subscribe(resp => {
        instance.selectedRoom = null;
        instance.getRooms();
      });
    }
    if(instance.selectedMeeting != null) {
      instance.http.delete(data["endpoint"] + 'meeting/' + instance.selectedMeeting.uuid, instance.getHeader()).subscribe(resp => {
        instance.selectedMeeting = null;
        instance.getMeetings();
      });
    }
  }

}
