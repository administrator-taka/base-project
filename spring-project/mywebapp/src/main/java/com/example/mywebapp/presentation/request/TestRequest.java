package com.example.mywebapp.presentation.request;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class TestRequest {

  @JsonProperty("test")
  private String test;
}
