package com.fleet.monitor.consumer;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fleet.monitor.config.RabbitMQConfig;
import com.fleet.monitor.model.GpsMessage;
import com.fleet.monitor.repository.GpsDataRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Component
public class GpsConsumer {

    private static final Logger log = LoggerFactory.getLogger(GpsConsumer.class);

    private final GpsDataRepository gpsDataRepository;
    private final ObjectMapper objectMapper;

    public GpsConsumer(GpsDataRepository gpsDataRepository, ObjectMapper objectMapper) {
        this.gpsDataRepository = gpsDataRepository;
        this.objectMapper = objectMapper;
    }

    @RabbitListener(queues = RabbitMQConfig.GPS_QUEUE)
    public void consumeGps(String message) {
        try {
            GpsMessage gps = objectMapper.readValue(message, GpsMessage.class);
            gpsDataRepository.save(gps);
            log.info(
                    "GPS guardado: vehicleId={}, lat={}, lng={}, speed={}",
                    gps.getVehicleId(),
                    gps.getLat(),
                    gps.getLng(),
                    gps.getSpeed()
            );
        } catch (Exception e) {
            log.error("Error procesando GPS: {}", e.getMessage());
        }
    }

}
