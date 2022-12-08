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
demo_func(tick tick.cpp)


# For Cpp-python embeddings
if (CMAKE_SYSTEM_NAME STREQUAL "Wasm")
    set(PYTHON_LIBRARIES "dummy/libpython3.8.a")
    set(PYTHON_INCLUDE_DIRS dummy/python3.8) # TODO: Compile CPython target
else ()
    find_package(Python REQUIRED Development)
endif ()


add_executable(py_func py_func.cpp)

if (CMAKE_SYSTEM_NAME STREQUAL "Wasm")
    #    set_target_properties(py_func PROPERTIES LINK_FLAGS " \
    #    -s WASM=1 \
    #    -s TOTAL_MEMORY=1GB \
    #    -s GLOBAL_BASE=0 \
    #    -s STACK_SIZE=4MB \
    #    -s EXIT_RUNTIME=1 \
    #")
    target_link_libraries(py_func ${PYTHON_LIBRARIES})
    target_include_directories(py_func PUBLIC ${PYTHON_INCLUDE_DIRS})
else ()
    target_link_libraries(py_func PRIVATE Python::Python)
endif ()
