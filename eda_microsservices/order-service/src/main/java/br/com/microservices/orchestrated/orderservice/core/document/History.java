package br.com.microservices.orchestrated.orderservice.core.document;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class History {
    private String source; //Pode ser enum ou string
    private String status; //Só mapear enums para dados que vamos manipular (regras de negócio)
    private String message;
    private LocalDateTime createdAt;

}
