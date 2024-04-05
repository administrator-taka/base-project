package com.example.mywebapp.domain.logic;

import com.example.mywebapp.domain.model.TestModel;
import com.example.mywebapp.infrastructure.entity.TestEntity;
import com.example.mywebapp.infrastructure.mapper.TestMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class TestLogic {

  private final TestMapper testMapper;

  public TestModel test(String name) {
    TestEntity entity = testMapper.selectTest(name);
    TestModel model = new TestModel();
    model.setId(entity.getId());
    model.setName(entity.getName());
    model.setPassword(entity.getPassword());
    return model;

  }

}
