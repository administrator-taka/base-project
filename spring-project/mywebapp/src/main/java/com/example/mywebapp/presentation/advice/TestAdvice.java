package com.example.mywebapp.presentation.advice;

import java.lang.reflect.Type;
import javax.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.MethodParameter;
import org.springframework.http.HttpInputMessage;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;
import org.springframework.web.servlet.mvc.method.annotation.RequestBodyAdviceAdapter;

@RestControllerAdvice
@Slf4j
public class TestAdvice extends RequestBodyAdviceAdapter {

  @Override
  public boolean supports(MethodParameter methodParameter, Type targetType,
      Class<? extends HttpMessageConverter<?>> converterType) {
    return true; // すべてのリクエストをサポートする
  }

  @Override
  public Object afterBodyRead(Object body, HttpInputMessage inputMessage, MethodParameter parameter,
      Type targetType, Class<? extends HttpMessageConverter<?>> converterType) {

    HttpServletRequest request = ((ServletRequestAttributes) RequestContextHolder.getRequestAttributes()).getRequest();
    log.debug(body.toString());
    String ipAddress = request.getRemoteAddr();
    log.debug(ipAddress);
    log.debug("テストdebug");
    log.info("テストinfo");
    log.warn("テストwarn");
    log.error("テストerror");
    return super.afterBodyRead(body, inputMessage, parameter, targetType, converterType);
  }

}
