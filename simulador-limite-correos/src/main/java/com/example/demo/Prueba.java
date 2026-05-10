package com.example.demo;

import jakarta.mail.internet.MimeMessage;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;

@Service
public class Prueba {

    @Autowired
    private JavaMailSender mailSender;

    @Value("${app.mail.from:${spring.mail.username}}")
    private String emisor;

    @Value("${app.mail.to}")
    private String destinatario;

    @Value("${app.mail.delay-ms:1000}")
    private int tiempoEspera; // en milisegundos

    public void ejecutar() {
        boolean repetir = true;
        int contadorfallas = 0;
        int contadorCorreosEnviados = 1;

        do{
            try {

                // Crear y configurar el mensaje
                MimeMessage mensaje = mailSender.createMimeMessage();
                MimeMessageHelper helper = new MimeMessageHelper(mensaje, true, "UTF-8");

                helper.setTo(destinatario);
                helper.setSubject("Prueba de correo");
                helper.setText("Prueba numero: " + contadorCorreosEnviados);
                helper.setFrom(emisor);

                // Enviar el correo
                mailSender.send(mensaje);

                System.out.println("\nCorreo enviado numero " + contadorCorreosEnviados + "\n");
                contadorCorreosEnviados++;

            } catch (Exception e) {

                // Se incrementa el contador de fallas de correo
                contadorfallas++;

                System.out.println("----------------------------------------------------------------------\n");
                System.out.println("Error numero " + contadorfallas + " al enviar el correo");
                e.printStackTrace();
                System.out.println("----------------------------------------------------------------------\n\n");

                if(contadorfallas == 3){
                    repetir = false;
                }
            }

            // lo duerme durante un segundo
            try{
                Thread.sleep(tiempoEspera);
            }catch (InterruptedException exception){
                System.out.println("hubo un error en el thread al poner espera de un segundo");
                exception.printStackTrace();
                repetir = false;
            }


        }while(repetir);



    }

}
