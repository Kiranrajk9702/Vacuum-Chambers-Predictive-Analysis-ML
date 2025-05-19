create database equipment_maintenance;

use equipment_maintenance;

SELECT * FROM equipment_maintenance.predictive_maintenance;

-- View first 20 rows:
SELECT * FROM predictive_maintenance
 LIMIT 20;
 
 
 -- Count rows by failure type:
SELECT `Failure Type`, COUNT(*) AS count
FROM predictive_maintenance
GROUP BY `Failure Type`;

-- Average tool wear by product type:
SELECT Type, AVG(`Tool wear [min]`) AS avg_tool_wear
FROM predictive_maintenance
GROUP BY Type;

-- Summary statistics for numeric columns:
SELECT 
  AVG(`Air temperature [K]`) AS avg_air_temp,
  AVG(`Process temperature [K]`) AS avg_process_temp,
  AVG(`Rotational speed [rpm]`) AS avg_rotational_speed,
  AVG(`Torque [Nm]`) AS avg_torque,
  AVG(`Tool wear [min]`) AS avg_tool_wear
FROM predictive_maintenance;

-- Maximum and Minimum Process Temperature
SELECT 
  MAX(`Process temperature [K]`) AS max_process_temp,
  MIN(`Process temperature [K]`) AS min_process_temp
FROM predictive_maintenance;



SHOW COLUMNS FROM predictive_maintenance;

SELECT @@hostname;
SELECT USER();
