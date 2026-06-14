from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    HiddenField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
    TimeField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional, Regexp


class RegistrationForm(FlaskForm):
    index_number = StringField("index_number", validators=[DataRequired(), Regexp(r"^\d{6}$")])
    first_name = StringField("first_name", validators=[DataRequired(), Length(max=80)])
    last_name = StringField("last_name", validators=[DataRequired(), Length(max=80)])
    nickname = StringField("nickname", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("password", validators=[DataRequired(), Length(min=12, max=128)])
    confirm_password = PasswordField(
        "confirm_password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )
    major_id = SelectField("major", coerce=int, validators=[DataRequired()])
    study_level = SelectField(
        "study_level",
        choices=[
            ("first_cycle", "study_level_first_cycle"),
            ("second_cycle", "study_level_second_cycle"),
            ("long_cycle", "study_level_long_cycle"),
        ],
        validators=[DataRequired()],
    )
    study_mode = SelectField(
        "study_mode",
        choices=[
            ("full_time", "study_mode_full_time"),
            ("part_time", "study_mode_part_time"),
            ("puw", "study_mode_puw"),
        ],
        validators=[DataRequired()],
    )
    year_of_study = IntegerField("year_of_study", validators=[DataRequired(), NumberRange(min=1, max=5)])
    accept_terms = BooleanField("accept_terms", validators=[DataRequired()])
    accept_privacy = BooleanField("accept_privacy", validators=[DataRequired()])
    submit = SubmitField("register")


class LoginForm(FlaskForm):
    login = StringField("email", validators=[DataRequired(), Length(max=255)])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("login")


class ActivationForm(FlaskForm):
    code = StringField("activation_code", validators=[DataRequired(), Regexp(r"^\d{6}$")])
    submit = SubmitField("activate")


class ProfileForm(FlaskForm):
    first_name = StringField("first_name", validators=[DataRequired(), Length(max=80)])
    last_name = StringField("last_name", validators=[DataRequired(), Length(max=80)])
    nickname = StringField("nickname", validators=[DataRequired(), Length(min=3, max=80)])
    preferred_language = SelectField("language", choices=[("pl", "PL"), ("en", "EN")])
    submit = SubmitField("save")


class MembershipRequestForm(FlaskForm):
    club_id = HiddenField("club_id", validators=[DataRequired()])
    request_type = SelectField(
        "request_type",
        choices=[("join", "join_club"), ("already_member", "already_member")],
        validators=[DataRequired()],
    )
    submit = SubmitField("request_membership")


class ReservationForm(FlaskForm):
    club_id = SelectField("organization", coerce=int, validators=[DataRequired()])
    room_id = SelectField("room", coerce=int, validators=[DataRequired()])
    title = StringField("title", validators=[DataRequired(), Length(max=180)])
    description = TextAreaField("description", validators=[DataRequired(), Length(min=10, max=2000)])
    event_type = SelectField(
        "event_type",
        choices=[("meeting", "meeting"), ("workshop", "workshop"), ("presentation", "presentation")],
        validators=[DataRequired()],
    )
    date = DateField("date", validators=[DataRequired()])
    start_time = TimeField("start_time", validators=[DataRequired()])
    end_time = TimeField("end_time", validators=[DataRequired()])
    participants = IntegerField("participants", validators=[DataRequired(), NumberRange(min=1, max=400)])
    requires_step_free_access = BooleanField("step_free")
    requires_elevator = BooleanField("elevator")
    requires_induction_loop = BooleanField("induction_loop")
    requires_accessible_computer = BooleanField("accessible_computer")
    accessibility_notes = TextAreaField("accessibility_notes", validators=[Optional(), Length(max=1000)])
    submit = SubmitField("create_reservation")


class AdminDecisionForm(FlaskForm):
    action = HiddenField("action", validators=[DataRequired()])
    rejection_reason = TextAreaField("rejection_reason", validators=[Optional(), Length(max=1000)])
    club_role = SelectField(
        "role",
        choices=[
            ("member", "member"),
            ("chair", "chair"),
            ("vice_chair", "vice_chair"),
            ("secretary", "secretary"),
            ("treasurer", "treasurer"),
        ],
    )
    submit = SubmitField("save")
