package com.example.mywebapp.infrastructure.mapper;

import com.example.mywebapp.infrastructure.entity.TestEntity;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

@Mapper
public interface TestMapper {

  TestEntity selectTest(@Param("name") String name);
}