package com.example.mywebapp.presentation.controller;

import com.example.mywebapp.application.dto.TestDto;
import com.example.mywebapp.application.service.TestService;
import com.example.mywebapp.presentation.request.TestRequest;
import com.example.mywebapp.presentation.response.TestResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/test")
@RequiredArgsConstructor
public class TestController {

  private final TestService testService;

  @RequestMapping("/")
  public String home() {
    return "Hello World";
  }

  @PostMapping(path = "/db", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
  public ResponseEntity<?> test(@RequestBody TestRequest request) {
    TestDto dto = testService.test(request.getTest());
    TestResponse response = new TestResponse();
    response.setId(dto.getId());
    response.setName(dto.getName());
    response.setPassword(dto.getPassword());
    return ResponseEntity.status(HttpStatus.OK).body(response);
  }
}
