use uzistuff

insert into user (id, username, password_hash) values (1, 'John', 'pbkdf2:sha256:50000$JzEe85lG$f0a10c3d079bc7c988adb9779f8cd9df5828f9466e1547dd7e300e9497ef9086');
insert into user (id, username, password_hash) values (2, 'Alice', 'pbkdf2:sha256:50000$JzEe85lG$f0a10c3d079bc7c988adb9779f8cd9df5828f9466e1547dd7e300e9497ef9086');
insert into ru (id, name) values (1, 'NSK');
insert into ru (id, name) values (2, 'OMS');
insert into ru (id, name) values (3, 'SPB');
insert into ru (id, name) values (4, 'YAR');
insert into ru (id, name) values (5, 'KMR');
insert into ru (id, name) values (6, 'TUM');
insert into region_mgmt (id, name) values (1, 'Новосибирск');
insert into region_mgmt (id, name) values (2, 'Омск');
insert into region_mgmt (id, name) values (3, 'СПб');
insert into region_mgmt (id, name) values (4, 'Ярославль');
insert into region_mgmt (id, name) values (5, 'Кемерово');
insert into dzo (id, name, service, manager) values (1, 'Центр', 'Договор от 30.01.18', 'Кудашов');
insert into dzo (id, name, service, manager) values (2, 'НЕ-Центр', 'Договор не заключён', '');
insert into azs_type (id, azstype) values (1, 'АЗС');
insert into azs_type (id, azstype) values (2, 'ААЗС');
insert into azs_type (id, azstype) values (3, 'Смешанная');
insert into reasons (id, reason_name) values (1, 'В работе');
insert into reasons (id, reason_name) values (2, 'Демонтирована');
insert into reasons (id, reason_name) values (3, 'На реконструкции');
insert into reasons (id, reason_name) values (4, 'Сдана в аренду');
insert into prereasons (id, reason_name) values (1, 'В работе');
insert into prereasons (id, reason_name) values (2, 'Демонтирована');
insert into prereasons (id, reason_name) values (3, 'На реконструкции');
insert into prereasons (id, reason_name) values (4, 'Сдана в аренду');

insert into azs (id, sixdign, ru, num, hostname, user_added, address, dzo, azs_type, active) values (111314, 111314, 5, 314, 'AZS-KMR-111-CRYPTO-314', 2, 'Новокузнецк, Тольятти 34', 1, 2, True);
insert into azs (id, ru, num, hostname, user_added, address, dzo, azs_type, active) values (222222, 222222, 6, 222, 'AZS-TUM-222-CRYPTO-222', 1,'Тюмень, Гагарина 29', 2, 1, False);
insert into azs (id, ru, num, hostname, user_added, address, dzo, azs_type, active) values (333333, 333333, 3, 333, 'AZS-SPB-333-CRYPTO-333', 2,'Санкт-Петербург, Шушары', 2, 1, False);
insert into hardware (id, azs_id) values (111314, 111314);
insert into hardware (id, azs_id) values (222222, 222222);
insert into hardware (id, azs_id) values (333333, 333333);
insert into status (id, azs_id, active, reason) values (111314, 111314, True, 1);
insert into status (id, azs_id, active, reason) values (222222, 222222, False, 3);
insert into status (id, azs_id, active, reason) values (333333, 333333, False, 4);
