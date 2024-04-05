package com.example.mywebapp.application.service;

import com.example.mywebapp.application.dto.TestDto;
import com.example.mywebapp.domain.logic.TestLogic;
import com.example.mywebapp.domain.model.TestModel;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Transactional
@Service
@RequiredArgsConstructor
public class TestServiceImpl implements TestService {

  private final TestLogic testLogic;

  @Override
  public TestDto test(String name) {
    TestModel model = testLogic.test(name);
    TestDto dto = new TestDto();
    dto.setId(model.getId());
    dto.setName(model.getName());
    dto.setPassword(model.getPassword());
    return dto;
  }
}
