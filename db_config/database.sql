CREATE TABLE address_dir
(
  address_id bigserial NOT NULL,
  unit_no varchar(30),
  street_number varchar(30),
  street_name varchar(250),
  additional_info varchar(250),
  city varchar(50,)
  province varchar(50),
  postal_code varchar(10),
  login_id bigint NOT NULL,
  created_at timestamp,
  updated_at timestamp
);

ALTER TABLE address_dir ADD CONSTRAINT address_id
  PRIMARY KEY (address_id);

CREATE TABLE health_history
(
  checkup_id bigserial NOT NULL,
  login_id bigint,
  has_fever boolean,
  has_cough boolean,
  has_tiredness boolean,
  has_breath_shortness boolean,
  has_headache boolean,
  created_at timestamp,
  updated_at timestamp
);

ALTER TABLE health_history ADD CONSTRAINT checkup_id
  PRIMARY KEY (checkup_id);

CREATE TABLE login_details
(
  login_id bigserial NOT NULL,
  username varchar(25) UNIQUE,
  password varchar(25),
  is_active boolean,
  created_at timestamp,
  updated_at timestamp
);

ALTER TABLE login_details ADD CONSTRAINT login_id
  PRIMARY KEY (login_id);

CREATE TABLE request_details
(
  request_id bigserial NOT NULL,
  request_date timestamp,
  request_type varchar(200),
  request_information text,
  request_note text,
  requester_id bigint,
  volunteer_id bigint,
  transaction_id bigint,
  is_cancelled boolean,
  is_commenced boolean,
  is_completed boolean,
  created_at timestamp,
  updated_at timestamp
);

ALTER TABLE request_details ADD CONSTRAINT request_id
  PRIMARY KEY (request_id);

CREATE TABLE requester_details
(
  requester_id bigserial NOT NULL,
  requester_name varchar(125),
  requester_email varchar(125) UNIQUE,
  requester_phone varchar(15) UNIQUE,
  requester_age smallint,
  has_medical_condition boolean,
  login_id bigint NOT NULL,
  tokens bigint DEFAULT 0,
  created_at timestamp,
  updated_at timestamp
);

ALTER TABLE requester_details ADD CONSTRAINT pk_requester_details
  PRIMARY KEY (requester_id);

CREATE TABLE token_transactions
(
  transaction_id bigserial NOT NULL,
  volunteer_id bigint,
  requester_id bigint,
  request_id bigint,
  tokens bigint,
  is_complete boolean DEFAULT false,
  created_at timestamp,
  updated_at timestamp
);

ALTER TABLE token_transactions ADD CONSTRAINT transaction_id
  PRIMARY KEY (transaction_id);

CREATE TABLE volunteer_details
(
  volunteer_id bigserial NOT NULL,
  volunteer_name varchar(125),
  volunteer_email varchar(125) UNIQUE,
  volunteer_phone varchar(15) UNIQUE,
  volunteer_age smallint,
  login_id bigint NOT NULL,
  tokens bigint DEFAULT 0,
  created_at timestamp,
  updated_at timestamp
);

ALTER TABLE volunteer_details ADD CONSTRAINT volunteer_id
  PRIMARY KEY (volunteer_id);

ALTER TABLE address_dir ADD CONSTRAINT fk_address_dir_
  FOREIGN KEY (login_id) REFERENCES login_details (login_id) ON DELETE NO ACTION ON UPDATE CASCADE;

ALTER TABLE health_history ADD CONSTRAINT fk_health_history_
  FOREIGN KEY (login_id) REFERENCES login_details (login_id) ON DELETE NO ACTION ON UPDATE CASCADE;

ALTER TABLE request_details ADD CONSTRAINT fk_request_details_requester_id
  FOREIGN KEY (requester_id) REFERENCES requester_details (requester_id) ON DELETE NO ACTION ON UPDATE CASCADE;

ALTER TABLE request_details ADD CONSTRAINT fk_request_details_transaction_id
  FOREIGN KEY (transaction_id) REFERENCES token_transactions (transaction_id) ON DELETE NO ACTION ON UPDATE CASCADE;

ALTER TABLE request_details ADD CONSTRAINT fk_request_details_volunteer_id
  FOREIGN KEY (volunteer_id) REFERENCES volunteer_details (volunteer_id) ON DELETE NO ACTION ON UPDATE CASCADE;

ALTER TABLE requester_details ADD CONSTRAINT fk_requester_details_login_id
  FOREIGN KEY (login_id) REFERENCES login_details (login_id) ON DELETE NO ACTION ON UPDATE CASCADE;

ALTER TABLE token_transactions ADD CONSTRAINT fk_token_transactions_requester_id
  FOREIGN KEY (requester_id) REFERENCES requester_details (requester_id) ON DELETE NO ACTION ON UPDATE CASCADE;

ALTER TABLE token_transactions ADD CONSTRAINT fk_token_transactions_volunteer_id
  FOREIGN KEY (volunteer_id) REFERENCES volunteer_details (volunteer_id) ON DELETE NO ACTION ON UPDATE CASCADE;

ALTER TABLE volunteer_details ADD CONSTRAINT fk_volunteer_details_login_id
  FOREIGN KEY (login_id) REFERENCES login_details (login_id) ON DELETE NO ACTION ON UPDATE CASCADE;