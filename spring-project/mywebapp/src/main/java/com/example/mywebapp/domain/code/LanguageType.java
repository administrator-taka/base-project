package com.example.mywebapp.domain.code;

/**
 * 言語タイプ
 */
public enum LanguageType {

  Japanese("ja"),

  English("en"),

  Korean("ko");


  private String code;

  LanguageType(String code) {
    this.code = code;
  }

  public String getCode() {
    return code;
  }
}
