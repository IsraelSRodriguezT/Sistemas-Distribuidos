package com.fleet.monitor.repository;

import com.fleet.monitor.model.GpsMessage;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;
import java.util.Optional;

public interface GpsDataRepository extends JpaRepository<GpsMessage, Long> {

    List<GpsMessage> findTop20ByVehicleIdOrderByIdDesc(String vehicleId);

    Optional<GpsMessage> findTopByOrderByIdDesc();

    @Query("select count(distinct g.vehicleId) from GpsMessage g")
    long countDistinctVehicles();

}
