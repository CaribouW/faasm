set(FAASM_USER demo)

function(demo_func exec_name dir_path)
    faasm_func(${exec_name} ${dir_path})
    set(ALL_DEMO_FUNCS ${ALL_DEMO_FUNCS} ${exec_name} PARENT_SCOPE)
endfunction(demo_func)

function(demo_func_c exec_name dir_path)
    faasm_func_c(${exec_name} ${dir_path})
    set(ALL_DEMO_FUNCS ${ALL_DEMO_FUNCS} ${exec_name} PARENT_SCOPE)
endfunction(demo_func_c)

demo_func(heap heap.cpp)

# 23/09/2020 - removing simd
# WASM-only functions
if (CMAKE_SYSTEM_NAME STREQUAL "Wasm")
#    demo_func(emscripten_check emscripten_check.cpp)
#    target_link_libraries(emscripten_check emscripten)
    # TODO - fix BLAS check function
    # include_directories(/usr/local/faasm/llvm-sysroot/include/clapack)
    # demo_func_c(blas_check blas_check.c)
    # target_link_libraries(blas_check ${FAASM_BLAS_LIBS})
endif()

