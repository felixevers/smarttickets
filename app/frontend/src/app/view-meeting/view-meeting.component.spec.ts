import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewMeetingComponent } from './view-meeting.component';

describe('ViewMeetingComponent', () => {
  let component: ViewMeetingComponent;
  let fixture: ComponentFixture<ViewMeetingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ViewMeetingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ViewMeetingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
