package com.example.demo;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ConfigurationXD implements CommandLineRunner {

    private final Prueba prueba;

    public ConfigurationXD(Prueba prueba) {
        this.prueba = prueba;
    }

    @Override
    public void run(String... args) {
        prueba.ejecutar();
    }
}