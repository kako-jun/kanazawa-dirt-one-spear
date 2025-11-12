CREATE TABLE jockeys (
	jockey_id VARCHAR NOT NULL, 
	name VARCHAR NOT NULL, 
	name_normalized VARCHAR, 
	PRIMARY KEY (jockey_id)
);
CREATE UNIQUE INDEX ix_jockeys_name ON jockeys (name);
CREATE INDEX ix_jockeys_jockey_id ON jockeys (jockey_id);
CREATE INDEX ix_jockeys_name_normalized ON jockeys (name_normalized);
CREATE TABLE trainers (
	trainer_id VARCHAR NOT NULL, 
	name VARCHAR NOT NULL, 
	PRIMARY KEY (trainer_id)
);
CREATE INDEX ix_trainers_trainer_id ON trainers (trainer_id);
CREATE UNIQUE INDEX ix_trainers_name ON trainers (name);
CREATE TABLE horses (
	horse_id VARCHAR NOT NULL, 
	name VARCHAR NOT NULL, 
	birth_date VARCHAR, 
	age INTEGER, 
	gender VARCHAR, 
	coat_color VARCHAR, 
	sire_id VARCHAR, 
	dam_id VARCHAR, 
	broodmare_sire_id VARCHAR, 
	breeder VARCHAR, 
	is_runner BOOLEAN NOT NULL, 
	PRIMARY KEY (horse_id), 
	FOREIGN KEY(sire_id) REFERENCES horses (horse_id), 
	FOREIGN KEY(dam_id) REFERENCES horses (horse_id), 
	FOREIGN KEY(broodmare_sire_id) REFERENCES horses (horse_id)
);
CREATE INDEX ix_horses_dam_id ON horses (dam_id);
CREATE INDEX ix_horses_broodmare_sire_id ON horses (broodmare_sire_id);
CREATE INDEX ix_horses_horse_id ON horses (horse_id);
CREATE INDEX ix_horses_name ON horses (name);
CREATE INDEX ix_horses_sire_id ON horses (sire_id);
CREATE TABLE races (
	race_id VARCHAR NOT NULL, 
	date DATETIME NOT NULL, 
	race_number INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	subtitle VARCHAR, 
	distance INTEGER NOT NULL, 
	direction VARCHAR, 
	track_condition VARCHAR NOT NULL, 
	weather VARCHAR NOT NULL, 
	race_class VARCHAR, 
	race_category VARCHAR, 
	weight_system VARCHAR, 
	prize_money JSON, 
	betting_code VARCHAR, 
	PRIMARY KEY (race_id)
);
CREATE INDEX ix_races_race_id ON races (race_id);
CREATE INDEX ix_races_date ON races (date);
CREATE TABLE entries (
	entry_id VARCHAR NOT NULL, 
	race_id VARCHAR NOT NULL, 
	horse_id VARCHAR NOT NULL, 
	jockey_id VARCHAR NOT NULL, 
	trainer_id VARCHAR, 
	gate_number INTEGER NOT NULL, 
	horse_number INTEGER NOT NULL, 
	weight FLOAT NOT NULL, 
	horse_weight INTEGER, 
	weight_diff VARCHAR, 
	career_record VARCHAR, 
	detailed_record JSON, 
	best_time VARCHAR, 
	best_time_good_track VARCHAR, 
	past_results JSON, 
	odds FLOAT, 
	PRIMARY KEY (entry_id), 
	FOREIGN KEY(race_id) REFERENCES races (race_id), 
	FOREIGN KEY(horse_id) REFERENCES horses (horse_id), 
	FOREIGN KEY(jockey_id) REFERENCES jockeys (jockey_id), 
	FOREIGN KEY(trainer_id) REFERENCES trainers (trainer_id)
);
CREATE INDEX ix_entries_entry_id ON entries (entry_id);
CREATE INDEX ix_entries_horse_id ON entries (horse_id);
CREATE INDEX ix_entries_jockey_id ON entries (jockey_id);
CREATE INDEX ix_entries_trainer_id ON entries (trainer_id);
CREATE INDEX ix_entries_race_id ON entries (race_id);
CREATE TABLE predictions (
	prediction_id VARCHAR NOT NULL, 
	race_id VARCHAR NOT NULL, 
	first INTEGER NOT NULL, 
	second INTEGER NOT NULL, 
	third INTEGER NOT NULL, 
	confidence FLOAT NOT NULL, 
	model_version VARCHAR NOT NULL, 
	predicted_at DATETIME NOT NULL, 
	PRIMARY KEY (prediction_id), 
	FOREIGN KEY(race_id) REFERENCES races (race_id)
);
CREATE INDEX ix_predictions_prediction_id ON predictions (prediction_id);
CREATE UNIQUE INDEX ix_predictions_race_id ON predictions (race_id);
CREATE TABLE results (
	result_id VARCHAR NOT NULL, 
	race_id VARCHAR NOT NULL, 
	finish_order JSON, 
	first INTEGER, 
	second INTEGER, 
	third INTEGER, 
	corner_positions JSON, 
	payouts JSON, 
	payout_trifecta INTEGER, 
	prediction_hit BOOLEAN NOT NULL, 
	purchased BOOLEAN NOT NULL, 
	bet_amount INTEGER, 
	return_amount INTEGER, 
	recorded_at DATETIME NOT NULL, 
	memo TEXT, 
	PRIMARY KEY (result_id), 
	FOREIGN KEY(race_id) REFERENCES races (race_id)
);
CREATE UNIQUE INDEX ix_results_race_id ON results (race_id);
CREATE INDEX ix_results_recorded_at ON results (recorded_at);
CREATE INDEX ix_results_result_id ON results (result_id);
