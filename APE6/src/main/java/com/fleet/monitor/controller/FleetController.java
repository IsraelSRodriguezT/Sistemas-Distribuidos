package com.fleet.monitor.controller;

import com.fleet.monitor.model.GpsMessage;
import com.fleet.monitor.repository.GpsDataRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Date;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/fleet")
public class FleetController {

    private final GpsDataRepository gpsDataRepository;

    public FleetController(GpsDataRepository gpsDataRepository) {
        this.gpsDataRepository = gpsDataRepository;
    }

    @GetMapping("/status")
    public ResponseEntity<Map<String, Object>> getStatus() {
        Map<String, Object> status = new LinkedHashMap<>();
        status.put("totalVehicles", gpsDataRepository.countDistinctVehicles());
        status.put("totalReadings", gpsDataRepository.count());
        status.put(
                "lastUpdate",
                gpsDataRepository.findTopByOrderByIdDesc()
                        .map(GpsMessage::getTimestamp)
                        .orElse(null)
        );
        status.put("timestamp", new Date());
        return ResponseEntity.ok(status);
    }

    @GetMapping("/vehicle/{id}/telemetria")
    public ResponseEntity<List<GpsMessage>> getTelemetria(@PathVariable String id) {
        return ResponseEntity.ok(
                gpsDataRepository.findTop20ByVehicleIdOrderByIdDesc(id)
        );
    }

}

/*
 * Pruebas desde la terminal (puerto 8080):
 *
 * curl http://localhost:8080/api/fleet/status
 * curl http://localhost:8080/api/fleet/vehicle/VH-001/telemetria
 */
